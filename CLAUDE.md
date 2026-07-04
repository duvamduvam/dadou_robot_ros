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
- `WHEELS_CMD_VEL_ENABLED` (robot/robot_config.py) reste à `False` tant que le protocole
  caméra de la bascule cmd_vel n'a pas été exécuté (voir « Prochaines étapes »).

## État Phase 2 (2026-07-04) — migration mouvement vers les standards ROS

FAIT et validé en sim (tout est commité/poussé, CI verte, 123 tests unitaires) :
- **Simulation Gazebo Harmonic** : `conf/docker/sim/` (conteneur dédié x86),
  packages `robot_description` (URDF xacro + plugins gz) et `robot_sim` (monde, bridge, launch).
- **Chaîne cmd_vel** (`conf/ros2_dependencies/robot_drive`, package AUTONOME — aucun import
  dadou_utils_ros ni robot.*) : `wheels_bridge` (StringTime→Twist ; le fil ne porte que la
  VALEUR de la clé wheels) → `twist_mux` (remote 100 > anim 10, verrou `e_stop` latché,
  `use_stamped: false` obligatoire en Jazzy) → `twist_deadman` (zéros à 20 Hz si silence
  > 400 ms) → `/cmd_vel`.
- **wheels_node bi-mode** : legacy StringTime (défaut) ou `/cmd_vel` selon le drapeau.
  En mode cmd_vel : deadman local 400 ms conservé (ultime rempart), twist nul → `stop()`
  franc (le plancher MIN_PWM d'`update_cmd(0,0)` ferait ramper les roues).

## Commandes

```bash
.venv/bin/pytest -q                 # tests unitaires (host, sans ROS ni matériel)

# Simulation (GUI ; HEADLESS=true pour serveur seul) :
cd conf/docker/sim && docker compose -f docker-compose-sim.yml up -d
# Chaîne roues dans la sim :
docker exec -d dadou-sim-container bash -c 'source /opt/ros/$ROS_DISTRO/setup.sh && source /home/ros2_ws/install/setup.bash && ros2 launch robot_drive drive.launch.py use_sim_time:=true'
# Conduite clavier (publie /cmd_vel_remote via remap, prioritaire) :
docker exec -it dadou-sim-container bash -c 'source /opt/ros/$ROS_DISTRO/setup.sh && ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=cmd_vel_remote'

# Déploiement robot : Ansible dans ../dadou_utils_ros (rsync du checkout local, PAS de git sur le Pi).
# ssh alias `r` = pi@robot. Logs applicatifs : /home/ros2_ws/log/robot.log DANS le conteneur (pas stdout docker).
# Sentinelle de build : créer le fichier robot/change déclenche colcon build au (re)démarrage.
```

## Prochaines étapes (dans l'ordre)

1. **Protocole caméra — bascule cmd_vel** (roues hors sol, filmé) : passer
   `WHEELS_CMD_VEL_ENABLED=True`, déployer, puis vérifier : boutons télécommande
   (forward/back/left/right), slider vitesse (50 % → demi-vitesse), séquence avec roues
   (moon-walk), **kill de la chaîne en plein mouvement → arrêt < 1 s**, e-stop
   (`ros2 topic pub /e_stop std_msgs/msg/Bool "{data: true}"` — latché, publier false pour
   déverrouiller). En cas de doute : remettre le drapeau à False (retour legacy immédiat).
2. Calibrer `max_wheel_speed` réel (m/s à consigne 1.0) — mesurable à la caméra, distance/temps.
3. Action ROS 2 `PlayAnimation` (les pistes roues des séquences passeront par cmd_vel_anim).
4. Source unique des séquences JSON (côté robot, la télécommande interroge par service).
5. Affiner l'URDF depuis les plans FreeCAD (~/Nextcloud/dev/didier/plans).

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
