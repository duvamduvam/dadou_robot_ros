"""Modèle exécutable de la chaîne de sécurité matérielle (carte main-carrier).

Ce fichier N'EST PAS du code embarqué : c'est la carte électronique en Python,
pour que les tests puissent la brancher au VRAI code Wheels (injection pca9685)
et prouver le comportement AVANT que le cuivre n'existe. Si le schéma KiCad
change (main-carrier/generate_schematic.py), ce modèle doit changer avec lui —
c'est le contrat entre l'électronique et le logiciel.

Ce qui est modélisé, et pourquoi c'est chacun un composant réel du schéma :

- ``FakePca9685`` + ``OeChannel`` : la puce PCA9685 des roues (adresse 0x40).
  Deux comportements de la vraie puce que l'ancien FakePCA des tests ne
  pouvait PAS exprimer, et qui sont tout l'enjeu de la carte :
    1. les REGISTRES survivent à une coupure d'OE (OE force les sorties à 0
       mais ne touche pas les registres → un ré-enable rejoue l'ancien PWM) ;
    2. le bus I2C peut se figer (``hang()``) → toute lecture/écriture lève
       OSError, la puce GARDE sa dernière consigne, les roues continuent.
- ``Monostable74HC123`` : le chien de garde U6, monostable REDÉCLENCHABLE
  R13=560k / C4=1µF → T ≈ 250 ms. Tant que le battement arrive, WD_OK reste
  haut ; 250 ms de silence et il retombe.
- ``SafetyChain`` : le ET par diodes (D20/D21) → SAFE, la bascule D 74HC74
  (U7) dont le /CLR asynchrone est DOMINANT (maintenir ARM enfoncé ne peut
  pas forcer un réarmement), l'inverseur Q1 → OE_WHEELS, et la boucle 12 V
  purement électromécanique du coup-de-poing → relais 40 A.

La propagation est PARESSEUSE : chaque lecture d'état recalcule d'abord la
logique combinatoire (dont l'échéance du monostable, basée sur l'horloge
TimeUtils — la même que Wheels, donc monkeypatchable par la même fixture).
Un /CLR asynchrone n'attend pas de tick : dès que SAFE tombe, RUN tombe,
et c'est exactement ce que la paresse garantit à toute observation.
"""

from dadou_utils_ros.utils.time_utils import TimeUtils


class I2cBusHungError(OSError):
    """Le bus I2C ne répond plus (SDA bloqué bas, esclave planté…).

    Hérite d'OSError : c'est ce que lèvent les libs Adafruit/SMBus réelles.
    Le code de prod ne doit PAS avoir de traitement spécial — le point du
    test est justement que stop() ÉCHOUE et que le matériel rattrape.
    """


class OeChannel:
    """Un canal PWM du PCA9685, avec la distinction registre / broche physique.

    - ``duty_cycle`` (lecture/écriture) = le REGISTRE, à travers le bus I2C :
      c'est ce que voit le code Wheels, et ça lève si le bus est figé.
    - ``output`` = la BROCHE physique, ce que voit le SmartDrive : registre,
      sauf si OE est haut (sorties forcées à 0). Ne passe pas par le bus,
      ne lève jamais — les électrons se moquent de l'état du bus.
    """

    def __init__(self, pca):
        self._pca = pca
        self._register = 0

    @property
    def duty_cycle(self):
        self._pca._check_bus()
        return self._register

    @duty_cycle.setter
    def duty_cycle(self, value):
        self._pca._check_bus()
        self._register = value

    @property
    def output(self):
        if self._pca.oe_high:
            return 0
        return self._register


class FakePca9685:
    """La puce PCA9685 des roues, avec sa broche OE et son bus débranchable."""

    def __init__(self):
        self.channels = [OeChannel(self) for _ in range(16)]
        self.frequency = None
        self.hung = False
        # La source d'OE est câblée après construction (wire_oe) : à la mise
        # sous tension, R10 tire OE à +5V → sorties coupées par défaut.
        self._oe_source = None

    def hang(self):
        """Fige le bus : à partir de maintenant tout accès I2C lève."""
        self.hung = True

    def _check_bus(self):
        if self.hung:
            raise I2cBusHungError("bus I2C figé : la puce ne répond plus")

    def wire_oe(self, chain):
        """Relie la broche OE à la chaîne de sécurité (le fil OE_WHEELS)."""
        self._oe_source = chain

    @property
    def oe_high(self):
        # Sans chaîne câblée : R10 tire OE haut, sorties coupées (fail-safe).
        if self._oe_source is None:
            return True
        return not self._oe_source.run


class Monostable74HC123:
    """U6 : monostable redéclenchable, R13=560k / C4=1µF → T ≈ 250 ms.

    Chaque impulsion de battement recharge la temporisation. Le silence
    la laisse expirer : WD_OK retombe et ne remonte qu'à l'impulsion suivante.
    """

    PERIOD_MS = 250

    def __init__(self):
        # Jamais impulsé = expiré : à la mise sous tension WD_OK est BAS
        # (personne n'a encore battu), la chaîne démarre désarmée.
        self._last_pulse = None

    def pulse(self):
        self._last_pulse = TimeUtils.current_milli_time()

    @property
    def wd_ok(self):
        if self._last_pulse is None:
            return False
        return TimeUtils.current_milli_time() - self._last_pulse < self.PERIOD_MS


class SafetyChain:
    """La chaîne complète : watchdog → ET diodes → bascule D → Q1 → OE + relais.

    Interface côté test :
    - ``heartbeat()``      : une impulsion HEARTBEAT (GPIO26) — le contrat
                             logiciel est de ne l'émettre qu'APRÈS une
                             écriture I2C réussie.
    - ``press_arm()``      : appui sur le bouton ARM (front d'horloge de U7).
    - ``press_estop()`` / ``release_estop()`` : le coup-de-poing (boucle NC).
    - ``run``              : sortie Q de la bascule (True = roues autorisées).
    - ``relay_closed``     : le relais 40 A de puissance (boucle 12 V pure,
                             indépendante de toute logique).
    """

    def __init__(self, pca):
        self._pca = pca
        self.watchdog = Monostable74HC123()
        self._estop_pressed = False
        self._run = False
        pca.wire_oe(self)

    # ---- signaux combinatoires -------------------------------------------

    @property
    def wd_ok(self):
        return self.watchdog.wd_ok

    @property
    def estop_ok(self):
        return not self._estop_pressed

    @property
    def safe(self):
        # D20/D21 : ET par diodes. Une seule condition qui tombe suffit.
        return self.wd_ok and self.estop_ok

    # ---- la bascule D (74HC74), /CLR asynchrone DOMINANT ------------------

    def _propagate(self):
        # /CLR asynchrone : dès que SAFE est bas, Q tombe — sans horloge,
        # sans délai, et quoi que fasse l'entrée ARM. C'est la dominance.
        if not self.safe:
            self._run = False

    @property
    def run(self):
        self._propagate()
        return self._run

    def press_arm(self):
        """Front montant sur l'horloge de U7 : D=+5V n'est mémorisé QUE si
        /CLR est relâché (SAFE haut). ARM maintenu enfoncé ne produit qu'un
        seul front — le maintenir ne sert à rien, c'est voulu."""
        self._propagate()
        if self.safe:
            self._run = True

    # ---- entrées physiques -------------------------------------------------
    #
    # PIÈGE DU MODÈLE (trouvé par les tests eux-mêmes) : la propagation
    # paresseuse perd les défauts TRANSITOIRES — si personne ne lit la chaîne
    # pendant que SAFE est bas, le /CLR n'est jamais rejoué et la bascule
    # « oublie » d'être tombée. Le vrai 74HC74 n'a pas besoin d'observateur.
    # Parade : tout événement qui peut faire REMONTER SAFE (retour du
    # battement, relâchement du champignon) propage d'abord l'état ANCIEN,
    # pour rejouer le /CLR avant d'effacer la preuve du défaut.

    def heartbeat(self):
        self._propagate()          # si le monostable avait expiré : Q tombe d'abord
        self.watchdog.pulse()

    def press_estop(self):
        self._estop_pressed = True
        self._propagate()          # /CLR immédiat : asynchrone, pas d'horloge

    def release_estop(self):
        self._propagate()          # rejouer la chute pendant l'appui...
        self._estop_pressed = False  # ...avant de refermer la boucle NC

    # ---- sorties physiques -------------------------------------------------

    @property
    def wheels_enabled(self):
        """L'état réel de la broche OE du PCA roues (via l'inverseur Q1)."""
        return self.run

    @property
    def relay_closed(self):
        """Le relais 40 A : bobine alimentée à travers la boucle NC du
        coup-de-poing. PUREMENT électromécanique : aucun logiciel, aucune
        logique — appuyer coupe la puissance, catégorie 0."""
        return self.estop_ok
