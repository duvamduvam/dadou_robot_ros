# Chantiers — tableau de bord

*Le point d'entrée du pilotage : statut, prochaine action et verrous de chaque
chantier. Créé le 2026-07-12 en dégraissant CLAUDE.md (qui était devenu un
journal de bord illisible).*

**Convention de tenue** (pour que ça ne se re-dégrade pas) :
- Chaque lot terminé met à jour **sa ligne** du tableau et **sa section** ici —
  pas CLAUDE.md (qui ne garde que les règles, commandes et priorités de tête).
- Le détail des décisions vit dans le **doc du chantier** (`etude-*.md`) ;
  ici, l'état et la prochaine action ; dans les **commits**, l'historique.
- Un chantier clos passe dans sa section avec la mention CLOS + date, et sort
  du tableau au bout d'un moment.

## Vue d'ensemble

| Chantier | Statut | Prochaine action | Verrou / condition |
|---|---|---|---|
| **0. Conversation (chat_node V2)** | code COMPLET, validé sim ; jamais testé matériel | protocole physique complet (conversation au casque, caméra à l'appui) | rebuild image ARM vision ; Pi 5 sur alim 27 W |
| **1. Test scénique au sol** | À FAIRE — première fois que cmd_vel roule au sol | séquence de spectacle complète, télécommande en main | — (c'est LUI le verrou des autres) |
| Interface web / télé-présence | W0 + console + W3-sim FAITS ; bringup réel actif (sans drive) | W1 : source e_stop + coup-de-poing sans fil | roues web réel ⟸ test scénique (1) + protocole caméra dédié |
| Télédiagnostic par agent IA | plan décidé ; étape 1 « trousse d'atelier » FAITE | étape 2 : boîte noire rosbag + bouton START | étape 3 ⟸ RAM du Pi 4 à relever (`ssh r 'cat /proc/meminfo'`) |
| Déclenchement conversation (intention de communiquer) | étude ÉCRITE, plan PROPOSÉ (pas grillé) | griller le plan (`/grill-me`) puis lot D0 | protocole physique chat_node V2 (0) d'abord |
| Suivi de personne (roues) | validé sim 5/5, déployé, **SIM-ONLY** | — (attend ses verrous) | test scénique (1) PUIS protocole caméra (`direction_sign` inconnu) |
| Gaze V1 + arbitrage actionneurs | validé RÉEL 12/07 ; arbitrage déployé sur les 2 Pi | vérif visuelle : gaze ON pendant une séquence (la tête ne doit plus trembler) | — |
| Fond de tiroir | — | voir §Fond de tiroir | — |

## 0. Conversation — protocole physique chat_node V2

Le code est COMPLET et commité (nuit du 10 au 11/07 : ~15 commits sur les
3 dépôts, validé en sim — bras+yeux bougent sur l'animation « parle », vu par
David dans Gazebo). Côté vision : chat_node (`chat_enabled:=true`, défaut
false), pipeline VAD→whisper→OpenRouter→piper→mixette, didascalies/émotions →
topics face+animation. Côté robot : fix MODE (dadou_utils_ros 5aefdf1 — le
mode random servo était mort depuis sept. 2025), expression « parle »,
séquence didier/parle.json.

**À faire sur le vrai matériel** : rebuild image ARM vision (voix piper +
whisper préchargés), Pi 5 avec ALIM 27 W (crash constaté sur USB-C PC),
sentinelles robot/change + vision/CHANGE, dérouler une conversation complète
au casque, vérifier gestes/bouche/arrêts propres (caméra à l'appui). Vérifier
aussi le gate d'arbitrage en conversation réelle (voir chantier gaze).

## 1. Test scénique en conditions réelles

Roues AU SOL, télécommande physique en main (boutons, slider, gants), une
séquence de spectacle complète — **première fois que le mode cmd_vel roule au
sol**. Vérifier aussi le sens de rotation gauche/droite (le protocole roues
hors sol ne l'a validé qu'en marche avant symétrique).

C'est le verrou de : roues web au réel (chantier web), suivi de personne au
réel.

## Interface web / télé-présence

Plan : [`etude-interface-web.md`](etude-interface-web.md) (décidé 2026-07-11 —
ne pas re-trancher, inconnues §9).

FAIT : **W0** vérifiée en sim le 11/07 (package `robot_web` autonome — node
rclpy+aiohttp, whitelist sans roues/e_stop, session exclusive + heartbeat, UI
vanilla — 511 tests, protocole WS validé de bout en bout, `WEB=true` port
8765 ; 8088 = Superset sur le PC de dev). **Console + W3-sim** le même jour :
console de régie (vidéo + pad + recherche), caméra gz → MJPEG `/video`,
pilotage pad/manette → `cmd_vel_web` (twist_mux prio 50, plafond dur 0,5 m/s
backend, zéro unique à l'arrêt — vérifié e2e jusqu'à `/cmd_vel`) ;
`WEB_DRIVE=true` requis (défaut false) + chaîne roues à la main
(docs/operations.md). **Bringup robot câblé** (web_bridge dans
robot_app.launch.py, contenus/supervision seulement — drive non passé donc
false) ; image ARM rebuildée (python3-aiohttp + python3-pil). **Console
enrichie le 12/07 (déployé + vérifié)** : alias mDNS `didier.local` (service
`avahi-alias-didier`, source `conf/systemd/`, install docs/operations.md —
`/etc/avahi/hosts` ne publie PAS sur le réseau) + toggle **Parole IA** (topic
`chat` en whitelist technique, ON/OFF → chat_node du Pi vision, même contrat
que `gaze`).

**Suite : W1** (source e_stop + coup-de-poing sans fil). Le passage des roues
web au ROBOT RÉEL reste conditionné au test scénique au sol (chantier 1) et à
un protocole caméra dédié.

## Télédiagnostic par agent IA

Plan : [`etude-telediagnostic.md`](etude-telediagnostic.md) (**décidé, grillé
le 2026-07-12** — ne pas re-trancher, décisions §8 : hybride embarqué host Pi
+ PC atelier, Opus sur abonnement, START télécommande → topic `incident`,
boîte noire segments SD 30 j sans caméra, remédiations autonomes encadrées).

FAIT : **étape 1 « trousse d'atelier »** le 12/07 —
`conf/scripts/collect-incident.sh` (host du Pi, best-effort, testé de bout en
bout contre la sim ; piège corrigé : `ros2 node list` vide au premier appel du
daemon → retente), skill `/diag` (`.claude/skills/diag/SKILL.md`), journal
[`incidents/`](incidents/README.md) (post-mortem obligatoire). Part avec le
rsync habituel, rien à déployer. **Utilisable dès maintenant** : panne →
`ssh r '~/ros2_ws/src/*/conf/scripts/collect-incident.sh'` → session Claude
+ `/diag`.

**Suite : étape 2 « boîte noire + bouton »** (§9 du plan) : enregistreur
rosbag par segments SD 60 s + purge 30 j dans le bringup, topic `incident`,
bouton START télécommande (libre — GPIO D21 + manette USB ; côté
dadou_control_ros : l'ajouter à `PUBLISHER_LIST`) + boutons logiciels,
marqueur `INCIDENT` dans robot.log, endpoints `/api/logs` + `/health` sur le
pont web, topic santé publié par system_node. Validation en sim d'abord.
**Préalables de l'étape 3 (agent embarqué)** : RAM du Pi 4
(`ssh r 'cat /proc/meminfo'` — non documentée nulle part), charge d'une
investigation vs tick 20 Hz, santé/espace SD, 4G partagé en salle.

## Déclenchement de la conversation (intention de communiquer)

Étude : [`etude-declenchement-conversation.md`](etude-declenchement-conversation.md)
(écrite le 2026-07-12 — état de l'art HRI chiffré + architecture proposée,
**plan PAS ENCORE GRILLÉ**).

Le problème : le chat écoute en continu dès que le toggle est ON (VAD seul,
aucun lien perception) — inutilisable en déambulation. La proposition :
node `engagement_node` (Pi vision, FSM PRESENT→INTERESTED→ENGAGED→
IN_CONVERSATION→COOLDOWN sur trajectoire + arrêt en zone sociale), micro armé
par l'engagement, sessions de conversation avec timeout, escalade asymétrique
(regard généreux / parole conservatrice), JAMAIS les roues. Lots D0
(calibration distance + état chat en topic) → D1 (FSM sans perception
nouvelle, validée sim) → D2 (visage frontal) → D3 (invitation théâtrale +
première rue).

**Suite : griller le plan** (inconnues §7 de l'étude : CPU Pi 5 restant,
micro mono en rue, groupes, politique d'abordage). Verrou d'entrée : le
protocole physique chat_node V2 (chantier 0) doit passer d'abord.

## Suivi de personne aux roues

CODE COMPLET, VALIDÉ EN SIM 5/5 (11/07 soir) : chaîne `/vision/person_box`
(Pi vision : azimut + HAUTEUR de silhouette = proxy de distance monoculaire,
cf. dadou_vision_ros) → `person_follower` (logique pure
`robot/move/follow_control.py` testée : deadzones, plafonds durs ABS 0,5/1,0
bornant même les paramètres, slew, zéro franc sur perte de cible < 600 ms et
sur OFF, marche arrière interdite par défaut) → `cmd_vel_follow` → twist_mux
**prio 20** (remote 100 > web 50 > follow 20 > anim 10, contrat gelé
re-testé). Toggle topic `follow` "on"/"off", **OFF par défaut**, lancé À LA
MAIN, PAS dans le bringup. Validé sim : T1 désactivé=zéro mouvement,
T2 avance+rotation vers la personne (odom confirme le déplacement gz), T3 la
télécommande écrase et le suivi reprend, T4 perte=zéro franc puis silence,
T5 OFF=zéro unique. Code DÉPLOYÉ sur les Pi au déploiement complet du 12/07
(rsync Ansible + sentinelles).

**SIM-ONLY** : usage réel conditionné au test scénique au sol (chantier 1)
PUIS protocole caméra roues hors sol (`direction_sign` azimut→rotation
inconnu, comme l'était celui du gaze).

## Gaze V1 (cou + yeux) + arbitrage actionneurs

**Gaze : PROTOCOLE CAMÉRA FAIT ET VALIDÉ le 12/07** sur le vrai robot, David
en scène. Résultats gravés en défauts du node : cou `direction_sign=+1`
(boucle fermée AUTO-VALIDANTE : la caméra est sur la tête, l'azimut converge
vers 0 — un mauvais signe aurait divergé en butée), amorti `ema_alpha=0.15` /
`slew_max=1.5` (les valeurs initiales 0.4/3.0 oscillaient : retard de phase
EMA×2 + slew + rampe servo), YEUX ajoutés (2e instance de GazeControl,
gain 49 = plein débattement 1-99 comme les séquences, `eye_direction_sign=-1`
— montage MIROIR du cou, validé visuellement). Toujours lancé À LA MAIN (pas
dans robot_bringup), toggle topic `gaze` "on"/"off".

**Arbitrage amont FAIT le 12/07** (lots A+B de
[`etude-arbitrage-actionneurs.md`](etude-arbitrage-actionneurs.md), contrat +
validation §8) : `animations_node` publie l'état latché `animation_state`
(nom ou "", time=remaining_ms, TRANSIENT_LOCAL des DEUX côtés — un abonné
volatile raterait le latch), le gaze et le chat (Pi vision, module pur
`vision/ai/arbitration.py`) se TAISENT quand une séquence a la main, avec
PÉREMPTION façon deadman (remaining+2 s) si animations_node meurt en pleine
séquence. Chat : rattrapage idle() après abandon STT (fini le visage coincé
sur « reflechit ») + stop ciblé (fini le stop GLOBAL qui tuait la séquence en
cours). Validé en sim 5/5 (latch, silence pendant séquence — contre-preuve
sans piste neck —, reprise, redémarrage en cours de séquence, péremption sur
kill). **DÉPLOYÉ ET VÉRIFIÉ sur les deux Pi le 12/07** : contrat joué en réel
("" latché au repos → "parle" time=4999 pendant une séquence de 5 s → "" au
retour), module arbitration + câblage péremption confirmés dans l'install du
Pi vision. Arbitrage aval par source différé (étude §5.3).

**Reste** : vérif VISUELLE comportementale à la prochaine session robot —
gaze ON pendant une séquence (la tête ne doit plus trembler), et le gate chat
en conversation réelle (avec le chantier 0).

## Fond de tiroir (pas urgents, pas oubliés)

- Calibrer `max_wheel_speed` réel (m/s à consigne 1.0) — mesurable à la
  caméra, distance/temps. Débloque le plafond de vitesse distant (web §2.3).
- Action ROS 2 `PlayAnimation` (les pistes roues des séquences passeront par
  cmd_vel_anim).
- Source unique des séquences JSON (côté robot, la télécommande interroge par
  service).
- Affiner l'URDF depuis les plans FreeCAD (~/Nextcloud/dev/didier/plans).
- Quirk latent à vérifier caméra un jour : en legacy, une paire [0,0] de
  séquence passe par update_cmd(0,0) → PWM au plancher MIN_PWM=5000 (rampage
  lent possible).
- Batterie : aucun capteur câblé — parqué vers le chantier élec (cartes PCB),
  décision télédiagnostic §8.
