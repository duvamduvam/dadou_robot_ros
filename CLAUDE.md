# Didier — robot de théâtre (dadou_robot_ros)

Code embarqué (Raspberry Pi 4, Docker, ROS 2 **Jazzy**) du robot de théâtre Didier (~50 kg).
Dépôts frères : `../dadou_control_ros` (télécommande), `../dadou_utils_ros` (lib partagée
par symlink + système de déploiement Ansible), `../dadou_vision_ros` (gelé).
Objectif long terme : robot autonome qui suit l'acteur, parle, simule des émotions.

## RÈGLES DE SÉCURITÉ (non négociables — des incidents roues ont déjà eu lieu)

- Toute fonctionnalité mouvement DOIT traiter son cas d'arrêt (deadman, e-stop, perte de liaison).
- Toute modification du chemin roues → validation en **simulation** d'abord, puis **protocole
  caméra** sur le vrai robot (roues hors sol, webcam USB, captures ffmpeg) AVANT usage au sol.
- `ROS_DOMAIN_ID=42` = vrai robot, `43` = simulation. Ne jamais mélanger : une commande de
  test ne doit jamais pouvoir atteindre le vrai Didier.
- Commiter un instantané AVANT tout refactoring.
- `WHEELS_CMD_VEL_ENABLED=True` est la config officielle depuis la bascule validée du
  2026-07-04 ; tout retour en arrière ou nouvelle bascule repasse par le protocole caméra.

## État Phase 2 (2026-07-04) — migration mouvement vers les standards ROS

FAIT et validé en sim (tout est commité/poussé, CI verte, 123 tests unitaires) :
- **Simulation Gazebo Harmonic** : `conf/docker/sim/` (conteneur dédié x86),
  packages `robot_description` (URDF xacro + plugins gz) et `robot_sim` (monde, bridge, launch).
- **Chaîne cmd_vel** (`conf/ros2_dependencies/robot_drive`, package AUTONOME — aucun import
  dadou_utils_ros ni robot.*) : `wheels_bridge` (StringTime→Twist ; le fil ne porte que la
  VALEUR de la clé wheels) → `twist_mux` (remote 100 > anim 10, verrou `e_stop` latché,
  `use_stamped: false` obligatoire en Jazzy) → `twist_deadman` (zéros à 20 Hz si silence
  > 400 ms) → `/cmd_vel`.
- **wheels_node bi-mode** : legacy StringTime ou `/cmd_vel` selon le drapeau.
  En mode cmd_vel : deadman local 400 ms conservé (ultime rempart), twist nul → `stop()`
  franc (le plancher MIN_PWM d'`update_cmd(0,0)` ferait ramper les roues), appelé une
  seule fois par arrêt (le twist_deadman inonde de zéros à 20 Hz au repos → spam log sinon).
- **BASCULE FAITE ET VALIDÉE sur le robot le 2026-07-04** : `WHEELS_CMD_VEL_ENABLED=True`
  est la config officielle. Protocole caméra 4/4 (roues hors sol) : forward 50 %,
  slider vitesse 50 %→25 %, e-stop étanche, kill de la chaîne en plein mouvement →
  arrêt local en 440 ms. Protocole rejouable : `conf/scripts/validate-cmdvel-protocol.sh`
  (à exécuter dans le conteneur robot). Rollback : drapeau à False + sentinelle + restart.

## État du 2026-07-11 — visage calibré, architecture assainie, temps réel

- **Câblage LED du visage ÉTABLI physiquement** (mires lues par l'humain — la webcam ne
  résout pas les motifs) et GRAVÉ dans `robot/visual/image_mapping.py` +
  `test_image_mapping.py` : bouche en serpentin entrant en bas-droite, rangée basse et
  yeux montés tête-bêche, œil droit 384-447 / gauche 448-511 (contigu, sans trous).
  Ne JAMAIS « corriger » ces tests sans repasser les mires (`calib`, `calib-couleurs`,
  `calib-bords` — voir docs/operations.md).
- **Chantier architecture fait** : code mort purgé, décodage StringTime commun (payload
  JSON invalide = refus loggué, plus de perte silencieuse), classe `Track` unique pour
  les pistes de keyframes (fix au passage : les frames du visage étaient décalées d'un
  cran), contrat `Action` (ABC), contrats de données testés (chaque visuel/audio/brique
  référencé doit exister). **443 tests** (`.venv/bin/pytest -q`), CI verte.
- **Temps réel fait** : `FastNeoPixel` (transmission sans le sleep de 31 ms de Blinka —
  mesuré 32,6 → 1,3 ms bloqués par show), tick global 20 Hz (`TICK_PERIOD_S`, chaîne
  roues non touchée), servos en rampe linéaire (`RAMP_SPEED=160`, à caler sur scène) +
  anti-spam I2C + deadman façon roues + fix `random_duration` (le réel suit enfin la sim).
- ⚠️ **`e_stop` n'a AUCUNE source** (verrou twist_mux déclaré, personne ne publie —
  vérifié robot + télécommande). Le deadman 400 ms est l'arrêt d'urgence effectif.
  À câbler côté télécommande, avec protocole roues.
- ⚠️ **`chat_node` coupé** sur le Pi vision depuis le 11/07 (il écrase `face` au moindre
  bruit). Relance : `ssh pi@192.168.1.151 'sudo docker restart dadou-vision-container'`.

## Commandes

```bash
.venv/bin/pytest -q                 # tests unitaires (host, sans ROS ni matériel)

# Simulation (GUI ; HEADLESS=true pour serveur seul ; ANIMATIONS=true = animations_node en sim) :
cd conf/docker/sim && ANIMATIONS=true docker compose -f docker-compose-sim.yml up -d
# Jouer une animation en sim (bras/yeux/cou via servos_sim_node — validé 2026-07-11) :
docker exec dadou-sim-container bash -c 'source /opt/ros/$ROS_DISTRO/setup.sh && source /home/ros2_ws/install/setup.bash && ros2 topic pub --once animation robot_interfaces/msg/StringTime "{msg: \"\\\"parle\\\"\", time: 45000, anim: false}"'
# Arrêt d'animation : msg: "false" (booléen JSON — PAS "stop", qui serait cherché comme nom de séquence).
# Chaîne roues dans la sim :
docker exec -d dadou-sim-container bash -c 'source /opt/ros/$ROS_DISTRO/setup.sh && source /home/ros2_ws/install/setup.bash && ros2 launch robot_drive drive.launch.py use_sim_time:=true'
# Conduite clavier (publie /cmd_vel_remote via remap, prioritaire) :
docker exec -it dadou-sim-container bash -c 'source /opt/ros/$ROS_DISTRO/setup.sh && ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=cmd_vel_remote'
# Suivi de personne en sim (chaîne roues requise ; toggle topic `follow` on/off, OFF par défaut) :
docker exec -d dadou-sim-container bash -c 'source /opt/ros/$ROS_DISTRO/setup.sh && source /home/ros2_ws/install/setup.bash && ros2 run robot person_follower'
# Perception scriptée pour le tester (personne à droite, loin, sûre) :
docker exec -d dadou-sim-container bash -c 'source /opt/ros/$ROS_DISTRO/setup.sh && ros2 topic pub -r 16 /vision/person_box geometry_msgs/msg/PointStamped "{point: {x: 0.5, y: 0.2, z: 0.9}}"'

# Déploiement robot : Ansible dans ../dadou_utils_ros (rsync du checkout local, PAS de git sur le Pi).
# ssh alias `r` = pi@robot. Logs applicatifs : /home/ros2_ws/log/robot.log DANS le conteneur (pas stdout docker).
# Sentinelle de build : créer le fichier robot/change déclenche colcon build au (re)démarrage.
```

## Prochaines étapes (dans l'ordre)

En parallèle des priorités 0-1 : **chantier interface web / télé-présence** (plan
complet cadré le 2026-07-11 — `docs/etude-interface-web.md`). **W0 FAITE et vérifiée
en sim le 2026-07-11** : package `robot_web` autonome (node rclpy+aiohttp, whitelist
sans roues/e_stop, session exclusive + heartbeat, UI vanilla), 511 tests, protocole
WS validé de bout en bout dans le conteneur sim (`WEB=true`, port 8765 — 8088 =
Superset sur le PC de dev). **Console + W3-sim FAITES le même jour** : refonte UI
(console de régie : vidéo + pad + recherche), caméra gz sur le robot simulé →
MJPEG `/video`, pilotage pad/manette → `cmd_vel_web` (twist_mux prio 50, plafond
dur 0,5 m/s backend, zéro unique à l'arrêt — vérifié e2e jusqu'à `/cmd_vel`).
`WEB_DRIVE=true` requis (défaut false) + chaîne roues lancée à la main (voir
docs/operations.md). **Bringup robot câblé** (web_bridge dans robot_app.launch.py,
contenus/supervision seulement — drive non passé donc false) : au prochain
déploiement, REBUILD image ARM requis (python3-aiohttp + python3-pil ajoutés à
packages-docker.txt) ; procédure sim→réel dans docs/operations.md. Suite : W1
(source e_stop + coup-de-poing) ; le passage des roues web au ROBOT RÉEL reste
conditionné au test scénique au sol (priorité 1) et à un protocole caméra dédié.

**Suivi de personne AUX ROUES (2026-07-11 soir) — CODE COMPLET, VALIDÉ EN SIM 5/5** :
chaîne `/vision/person_box` (Pi vision : azimut + HAUTEUR de silhouette = proxy de
distance monoculaire, cf. dadou_vision_ros) → `person_follower` (logique pure
`robot/move/follow_control.py` testée : deadzones, plafonds durs ABS 0,5/1,0
bornant même les paramètres, slew, zéro franc sur perte de cible < 600 ms et sur
OFF, marche arrière interdite par défaut) → `cmd_vel_follow` → twist_mux **prio
20** (remote 100 > web 50 > follow 20 > anim 10, contrat gelé re-testé). Toggle
topic `follow` "on"/"off", **OFF par défaut**, lancé À LA MAIN, PAS dans le
bringup. Validé sim : T1 désactivé=zéro mouvement, T2 avance+rotation vers la
personne (odom confirme le déplacement gz), T3 la télécommande écrase et le
suivi reprend, T4 perte=zéro franc puis silence, T5 OFF=zéro unique.
**SIM-ONLY** : usage réel conditionné au test scénique au sol (priorité 1) PUIS
protocole caméra roues hors sol (`direction_sign` azimut→rotation inconnu,
comme le gaze). ⚠️ PAS DÉPLOYÉ sur les Pi (éteints au moment du déploiement) :
scp follow_control/person_follower/twist_mux.yaml/setup.py + sentinelles.

0. **Protocole physique chat_node V2 (conversation)** : le code est COMPLET et commité
   (nuit du 10 au 11/07 : ~15 commits sur les 3 dépôts, validé en sim — bras+yeux bougent
   sur l'animation « parle », vu par David dans Gazebo). Côté vision : chat_node
   (chat_enabled:=true, défaut false), pipeline VAD→whisper→OpenRouter→piper→mixette,
   didascalies/émotions → topics face+animation. Côté robot : fix MODE (dadou_utils_ros
   5aefdf1 — le mode random servo était mort depuis sept. 2025), expression « parle »,
   séquence didier/parle.json. À faire sur le vrai matériel : rebuild image ARM vision
   (voix piper + whisper préchargés), Pi 5 avec ALIM 27 W (crash constaté sur USB-C PC),
   sentinelles robot/change + vision/CHANGE, dérouler une conversation complète au casque,
   vérifier gestes/bouche/arrêts propres (caméra à l'appui).
1. **Test scénique en conditions réelles** : roues AU SOL, télécommande physique en main
   (boutons, slider, gants), une séquence de spectacle complète — première fois que le
   mode cmd_vel roule au sol. Vérifier aussi le sens de rotation gauche/droite (le
   protocole roues hors sol ne l'a validé qu'en marche avant symétrique).
2. **Protocole caméra du cou (gaze V1)** : la chaîne webcam→/vision/person (Pi 5, tourne
   en prod, validée personne réelle 16 Hz) → gaze_follower (55676b6, validé sim, OFF par
   défaut, lancé À LA MAIN — pas dans robot_bringup) est prête. À valider sur le vrai
   robot : `direction_sign` (sens azimut→cou INCONNU), amplitude (gain=20 ≈ ±37°),
   sortie StringTime `neck` jamais exercée en réel, arbitrage animations↔gaze (les deux
   écrivent `neck` — en attendant : gaze OFF pendant les séquences). Toggle : topic
   StringTime `gaze` "on"/"off".
3. Calibrer `max_wheel_speed` réel (m/s à consigne 1.0) — mesurable à la caméra, distance/temps.
4. Action ROS 2 `PlayAnimation` (les pistes roues des séquences passeront par cmd_vel_anim).
4. Source unique des séquences JSON (côté robot, la télécommande interroge par service).
5. Affiner l'URDF depuis les plans FreeCAD (~/Nextcloud/dev/didier/plans).
6. Quirk latent à vérifier caméra un jour : en legacy, une paire [0,0] de séquence passe
   par update_cmd(0,0) → PWM au plancher MIN_PWM=5000 (rampage lent possible).

## Méthode de travail

- **Commenter chaque action en travaillant** (le quoi ET le pourquoi) : narration des
  étapes dans la conversation, commentaires français dans code/scripts/configs
  (les contraintes et pièges, pas la paraphrase), commits détaillés, découvertes
  consignées immédiatement. Raison : le projet doit pouvoir continuer avec un autre
  modèle (Opus) à tout moment — une action non expliquée est un fil perdu.
- Découpage modèles : conception/revue = modèle fort ; implémentation sur spec fermée =
  Agent Sonnet ; code sécurité = Agent Opus minimum ; mécanique = Haiku.
- Niveau d'effort en session Fable : **medium par défaut** (architecture, specs, revues,
  orchestration — le volume de raisonnement utile est modeste sur ce projet). Monter en
  **high** ponctuellement pour : conception d'un sous-système neuf (ros2_control,
  exécutif py_trees), débogage vraiment retors, revue finale d'un changement du chemin
  roues. `low` n'a pas d'intérêt : si la tâche est simple, autant basculer la session
  en Opus (moins cher que Fable bridé).
- La vérification doit exécuter le MÊME code que la prod (pas de reproduction approximative).
- CI GitHub Actions minimale (le repo est public : jamais de secrets, historique déjà purgé).
- Mémoire de session détaillée dans ~/.claude/projects/.../memory/ (chargée automatiquement).
