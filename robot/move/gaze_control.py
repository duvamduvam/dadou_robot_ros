"""Logique PURE du suivi du regard (gaze) — ZÉRO import ROS, entièrement testable.

Le robot suit une personne DU REGARD : ce module ne pilote QUE le cou (servo
`neck`, rotation panoramique autour de l'axe vertical). Il NE TOUCHE JAMAIS les
roues — aucune sortie ici ne concerne wheels/cmd_vel/e_stop (règle de sécurité
non négociable : télécommande > autonome, le regard ne déplace pas 50 kg).

Découpage volontaire (même philosophie que robot_drive) :
 - ICI : toute la logique de décision (mapping, lissage, slew, timeout, états),
   avec l'horloge passée en paramètre (now_ms) pour être testée sans ROS ni sleep.
 - DANS le node (gaze_follower_node.py) : uniquement les entrées/sorties ROS.

État machine :
 - IDLE    : pas de cible, cou au centre, on ne publie RIEN (le servo_node loggue
             chaque message reçu — inonder le topic au repos = spam de logs).
 - TRACKING: cible récente, on converge vers l'angle visé (slew rapide).
 - LOST    : cible perdue depuis > timeout → retour LENT au centre (slew réduit),
             puis IDLE une fois centré.
"""

import math

# Bornes matérielles de la consigne servo (voir robot/actions/servo.py :
# INPUT_MIN=0, INPUT_MAX=99, mappés 0->0°, 99->max_pos=180°). On ne sort JAMAIS
# de cette plage, même si des paramètres exotiques sont passés (garde-fou méca).
CONSIGNE_MIN = 0
CONSIGNE_MAX = 99

# États internes.
IDLE = "idle"
TRACKING = "tracking"
LOST = "lost"


def consigne_to_radians(consigne):
    """Convertit une consigne servo 0-99 en radians pour le joint `neck` de l'URDF.

    Chaîne de correspondance (documentée pour la revue) :
      - servo.py mappe 0-99 -> 0..180° matériel (max_pos=180, centre 50 -> ~90°) ;
      - dans l'URDF (dadou_robot.urdf.xacro) le joint `neck` est CENTRÉ :
        lower=-pi/2, upper=+pi/2. Donc 0° matériel = -pi/2, 90° = 0, 180° = +pi/2.
    D'où : rad = (consigne/99 - 0.5) * pi
      - consigne 0  -> -pi/2 (-1.5708)
      - consigne 50 -> +0.0159 rad (quasi 0 ; 50 n'est pas exactement le milieu
        de 0-99 qui vaut 49.5 — quirk hérité du "centre=50" de servo.py, négligeable)
      - consigne 99 -> +pi/2 (+1.5708)
    """
    return (consigne / 99.0 - 0.5) * math.pi


class GazeControl:
    """Logique de suivi du regard. Instancier une fois, appeler :
     - update(...) à CHAQUE message /vision/person reçu (cadence variable ~16 Hz) ;
     - tick(now_ms) à cadence FIXE (ex. 10 Hz) : renvoie la consigne cou 0-99 à
       publier, ou None s'il n'y a rien à publier (consigne inchangée / IDLE).
    """

    def __init__(self, center=50, gain=20, direction_sign=1, confidence_min=0.4,
                 ema_alpha=0.4, slew_max=3, slew_return=1, timeout_ms=1500,
                 enabled=False):
        # center=50 : position de repos du cou (regard droit devant).
        self.center = center
        # gain=20 : amplitude MAX de balayage (±20 autour du centre -> [30,70]).
        # Conservateur pour une première : ~±0.64 rad (~±37°) via le mapping ci-dessus.
        self.gain = gain
        # direction_sign=+1 : sens azimut -> cou. INCONNU MÉCANIQUEMENT tant que le
        # protocole caméra ne l'a pas tranché (même dette que le sens gauche/droite
        # des roues, cf. CLAUDE.md « Prochaines étapes »). +1 suppose : azimut +1
        # (personne au bord DROIT de l'image caméra) -> cou vers les consignes hautes.
        # À inverser en un seul paramètre si la caméra montre l'inverse.
        self.direction_sign = direction_sign
        # confidence_min=0.4 : sous ce seuil, la détection est jugée trop douteuse
        # pour bouger la tête (~plusieurs kg en haut du robot). Message ignoré, et
        # surtout il ne rafraîchit PAS le timeout -> une suite de détections faibles
        # finit par déclencher le retour au centre (LOST).
        self.confidence_min = confidence_min
        # Lissage EMA de l'azimut : amortit le bruit de la détection avant mapping.
        self.ema_alpha = ema_alpha
        # slew_max : variation MAX de consigne par tick en suivi (le servo saute
        # sinon instantanément à l'angle -> à-coups sur la mécanique de tête).
        self.slew_max = slew_max
        # slew_return : slew RÉDUIT pour le retour au centre en LOST (mouvement doux,
        # non urgent : plus personne à regarder).
        self.slew_return = slew_return
        # timeout_ms : sans détection valide depuis ce délai -> état LOST.
        self.timeout_ms = timeout_ms

        self.enabled = enabled
        self._reset()

    def _reset(self):
        """Remet toute la machine à l'état neutre (repos, plus aucune publication).
        Appelé au démarrage, sur désactivation, et sur "off" (reset complet exigé)."""
        self.position = float(self.center)   # position courante (float, slew continu)
        self.ema = None                       # azimut lissé (None = jamais vu)
        self.state = IDLE
        self.last_update_ms = None            # dernière détection VALIDE reçue
        self.last_published = None            # dernière consigne (int) réellement publiée

    def set_enabled(self, enabled):
        """Active/désactive le suivi. Désactivation = reset COMPLET de l'état
        (le node démarre désactivé : télécommande > autonome, toujours)."""
        self.enabled = enabled
        if not enabled:
            self._reset()

    def update(self, azimuth, elevation, confidence, now_ms):
        """À appeler à chaque message /vision/person.
        azimuth ∈ [-1..1] (+1 = bord droit image caméra), elevation ∈ [-1..1]
        (IGNORÉE : le cou ne fait que le panoramique, pas de joint de tilt pour
        l'instant), confidence ∈ [0..1]."""
        if not self.enabled:
            return
        # Détection trop peu sûre : on l'ignore ENTIÈREMENT (ni mouvement, ni
        # rafraîchissement du timeout) -> z=0.2 ne bouge pas la tête.
        if confidence < self.confidence_min:
            return
        # Lissage EMA (premier échantillon : on initialise directement dessus).
        if self.ema is None:
            self.ema = azimuth
        else:
            self.ema = self.ema_alpha * azimuth + (1.0 - self.ema_alpha) * self.ema
        self.last_update_ms = now_ms
        # (Ré)acquisition : depuis IDLE ou LOST on repart en suivi, en gardant la
        # position courante du cou (continuité du mouvement si on ré-attrape la cible).
        self.state = TRACKING

    def _target_tracking(self):
        """Consigne visée en suivi : centre + sens * gain * azimut_lissé, bornée
        à [centre-gain, centre+gain]."""
        raw = self.center + self.direction_sign * self.gain * self.ema
        low = self.center - self.gain
        high = self.center + self.gain
        return max(low, min(high, raw))

    def _slew_toward(self, target, step):
        """Rapproche self.position de target d'au plus `step` (protection méca)."""
        delta = target - self.position
        if abs(delta) <= step:
            self.position = float(target)
        elif delta > 0:
            self.position += step
        else:
            self.position -= step

    def tick(self, now_ms):
        """À appeler à cadence fixe. Renvoie la consigne 0-99 à publier, ou None."""
        # Désactivé : rien à publier et état réinitialisé (contrat de sécurité).
        if not self.enabled:
            self._reset()
            return None

        # Au repos absolu (jamais de cible, ou déjà recentré) : silence total.
        if self.state == IDLE:
            return None

        # Bascule TRACKING -> LOST si la cible n'a pas été rafraîchie à temps.
        if self.state == TRACKING and self.last_update_ms is not None:
            if now_ms - self.last_update_ms > self.timeout_ms:
                self.state = LOST

        if self.state == TRACKING:
            self._slew_toward(self._target_tracking(), self.slew_max)
        else:  # LOST : retour lent au centre.
            self._slew_toward(self.center, self.slew_return)
            if self.position == float(self.center):
                # Centré : on repassera IDLE, mais on laisse cette itération publier
                # la consigne centre finale (le cou doit finir droit devant).
                self.state = IDLE
                # On oublie l'azimut lissé : une PROCHAINE détection réamorcera l'EMA
                # à sa propre valeur (ré-acquisition franche, sans traîner l'ancienne
                # cible — sinon le cou repart d'abord vers l'ancien côté).
                self.ema = None

        # Consigne entière bornée aux limites servo (garde-fou méca).
        out = int(round(self.position))
        out = max(CONSIGNE_MIN, min(CONSIGNE_MAX, out))

        # Anti-spam : on ne republie que si la consigne a CHANGÉ (le servo_node
        # loggue chaque message ; à cible fixe et cou convergé -> plus rien).
        if out == self.last_published:
            return None
        self.last_published = out
        return out
