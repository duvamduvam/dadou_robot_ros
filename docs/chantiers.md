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
| Conversation en déambulation (intention + contenu) | plan DÉCIDÉ (grillé 12/07) ; D0 outillage + personas commutables FAITS 13/07 | campagne D0 (robot allumé) ; textes personas à valider avec David | D1+ ⟸ protocole physique chat_node V2 (0) ; D6 ⟸ verrous roues |
| Suivi de personne (roues) | validé sim 5/5, déployé, **SIM-ONLY** | — (attend ses verrous) | test scénique (1) PUIS protocole caméra (`direction_sign` inconnu) |
| Gaze V1 + arbitrage actionneurs | validé RÉEL 12/07 ; arbitrage déployé sur les 2 Pi | vérif visuelle : gaze ON pendant une séquence (la tête ne doit plus trembler) | — |
| Odométrie des roues (encodeurs) | plan DÉCIDÉ 14/07 ; **pièces 3D dessinées** ; rien acheté | commander les capteurs + imprimer le banc d'établi | **1 cote bloquante** : garde axe→châssis (§7) |
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

## Odométrie des roues

Plan : [`etude-odometrie.md`](etude-odometrie.md) (décidé 2026-07-14 — ne pas
re-trancher §3 à §6 ; inconnues §7).

**Le trou** : les roues n'ont AUCUN retour de rotation. Le moteur est un MY1016Z
**à balais** (la fiche matériel disait « brushless » — faux, corrigé le 14/07),
donc pas de capteurs Hall à dériver, et le SmartDrive40 n'expose aucune sortie
tachy. Conséquence : `/cmd_vel` est en **boucle ouverte** (des m/s qui sont du
PWM déguisé), et il n'y a pas de TF `odom` → `base_link`. C'est le verrou de
`ros2_control` ET de nav2. Ni le lidar ni la caméra ne le comblent.

**La solution retenue** : roue phonique lue par la FACE avec deux capteurs
inductifs `LJ12A3-4-Z/BX` (M12, NPN, 12 V) par roue → quadrature → PC847 → Pico
(PIO) → USB → nœud ROS. Carte montée **côté Pi**, pas près des roues (le signal
12 V à collecteur ouvert encaisse la distance ; le 3,3 V logique, non).

**Fixation — décidée le 14/07 d'après photos** : le disque se serre entre **deux
écrous sur la tige filetée** de l'axe (l'étude croyait à un rond Ø 20 lisse : c'est
faux, §2 corrigé). On ne touche **pas** aux 3 boulons de la couronne — c'est le
chemin de couple de la roue, et le disque ne transmet aucun couple.

**Pièces 3D dessinées** (`../plans/odometrie/`, dépôt plans b8243e9) : roue phonique
(porte-cibles PETG + 12 têtes de vis M8 en acier — l'inductif ne voit que le métal),
support capteurs nervuré, et le banc d'établi. Géométrie sous `assert()` : une cote
fausse refuse de compiler.

**Prochaine action — étape 1, sans robot, zéro risque** : commander les capteurs
(~15 €, cf. §9 — ⚠️ variante **NPN**, jamais PNP), imprimer le banc, passer la
réglette à la main devant les deux capteurs. Ça valide détection, entrefer, logique
inversée, quadrature et **le sens** (aller-retour), et tout le firmware Pico + le
nœud ROS se déboguent là.

**En parallèle, 5 mesures au pied à coulisse** (§7) — la bloquante est la **garde
axe → châssis** : elle plafonne le rayon du disque, donc la résolution.

Puis : étape 2 carte à trous au brochage définitif → étape 3 robot **roues hors
sol** + protocole caméra (on mesurera enfin la vraie vitesse pour un PWM donné,
première mesure objective du chemin roues) → étape 4 seulement, le PCB KiCad.

**Verrou** : trois cotes à mesurer avant de dimensionner le disque — diamètre
des roues, place libre sur l'axe, nombre de dents du pignon (+ pas de chaîne).

**Aval** : `ros2_control` / `diff_drive_controller`, EKF (encodeurs + IMU pour
le yaw), nav2. Le BNO055 existe déjà dans le code (`robot/move/bno_055_extended.py`)
mais n'est appelé nulle part en prod — vérifier s'il est encore sur le robot.

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

## Conversation en déambulation (intention de communiquer + contenu)

Plan : [`etude-declenchement-conversation.md`](etude-declenchement-conversation.md)
(**DÉCIDÉ, grillé le 2026-07-12** — ne pas re-trancher, décisions §5, points
ouverts §8). Périmètre élargi au grill : déclenchement + contenu + robustesse
rue.

Décisions clés : opérateur à vue, robot peut rouler → **regard généreux en
roulant, micro seulement à l'arrêt** (gate `/cmd_vel`) ; ENGAGED = personne
en zone sociale ET (arrêt ≥ 3 s OU parole détectée) — le bruit sans personne
ne déclenche plus jamais ; sessions (clôture silence 12 s / perte 3 s,
cooldown 45 s) ; **réactif d'abord** (invitation par le corps : regard +
expressions + gimmick sonore + animation « invite », rejet encaissé en jeu) ;
persona à créer de zéro (atelier d'écriture, garde-fous = confiance au modèle
pour l'instant, répliques courtes et relanceuses) ; micro U20 et CPU Pi 5
mesurés avant tout achat (soupape whisper API) ; latence < 2 s au premier
son ; corpus complet type tournage (affichage + bouton garder/effacer,
effacement par défaut). Abordage mobile, proactif verbal et mémoire des gens
en D6, derrière les verrous roues.

**D0 outillage FAIT le 13/07** (dadou_vision_ros 53c6d13, 162 tests) : topic
`chat_state` latché (listening/thinking/speaking/off), rejeu VAD de prod sur
wav (`vad_replay`), scripts `enregistre-rue.sh` / `mesure-cpu-conversation.sh`
/ `calibre-distance.sh`. **Atelier persona FAIT le 13/07** (partie écriture +
commutation) : 3 personnalités commutables à tester — « bougon » (défaut) /
« naif » / « vantard » — socle + textes dans `vision/ai/personas.py` (repo
public, tranché §8), commutation à chaud topic `persona` (nouvelle session de
conversation à chaque bascule), sélecteur sur la console web. **Suite : la
campagne D0** (robot allumé : mesure CPU en conversation, enregistrements rue
à rejouer, calibration distance) et la **validation des textes par David** ;
reste D3 : bouton télécommande, multi-langues, chrono latence. Verrou de
D1+ : protocole physique chat_node V2 (chantier 0). Réussite finale = grille
chiffrée du test rue D5 (§7 du plan).

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
- Micro réseau (ReSpeaker XVF3800 USB, ~94 €) — repéré et consigné dans
  `hardware/overview.md` §Microphone (2026-07-13, RIEN acheté). La décision de
  l'étude tient : on garde le U20 et on MESURE d'abord (lot D0). Deux choses
  rendent la question réelle quand même : la caméra CSI SUPPRIME le micro de la
  webcam, et l'étude ne traite nulle part l'ÉCHO (Didier parle fort → il
  s'entend et se répond ; c'est le mode de panne qui a fait couper chat_node le
  11/07). Half-duplex à implémenter de toute façon (gratuit). Pièges : XVF3000
  en fin de vie (prendre le 3800), jamais un HAT I2S (driver seeed-voicecard),
  l'AEC exige de re-router le TTS PAR le ReSpeaker, montage sur le CORPS (pas la
  tête : le repère DoA suivrait le gaze) et découplé mécaniquement.
- Détection d'obstacle (lidar 2D) — RPLIDAR C1 repéré (68,99 €) et contraintes de
  conception consignées dans `hardware/overview.md` §Distance & obstacle sensing
  (2026-07-13, RIEN acheté). Le trou n'est PAS la distance à la personne (déjà
  résolue par la hauteur de silhouette) mais l'obstacle qui n'est pas la personne.
  Points clés : pas besoin de 360° (arc AVANT suffit, secteur occulté à masquer),
  plan de scan BAS, barrière d'obstacle sur le Pi 4 dans la chaîne cmd_vel (jamais
  sur le Pi vision — une sécurité qui dépend du wifi n'en est pas une), CPU
  négligeable hors nav2. Pas avant la priorité 1 (test au sol) : c'est lui qui
  dira si l'opérateur au deadman suffit.
- Caméra CSI (nappe) à la place de la webcam USB — module IMX219 130° repéré et
  critères de tri consignés dans `hardware/overview.md` §Vision & camera
  (2026-07-13, RIEN acheté). Gain réel : la webcam plafonne à 16,7 fps alors que
  MediaPipe ne prend que 24 % de CPU. Trois coûts à ne pas oublier : la webcam
  EST le micro de chat_node V2 (→ micro USB à acheter), la nappe FPC traverserait
  le cou mobile (fatigue mécanique), et `cv2.VideoCapture` ne voit pas une CSI
  sur Pi 5 → libcamera/Picamera2 dans le conteneur vision. Ne pas lancer avant
  les priorités 0 et 1.
