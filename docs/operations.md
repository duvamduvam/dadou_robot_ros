# Operations & Rehearsal Checklist

## Deployment (workstation → robot)
- `cd conf && make d` — creates the `robot/change` build marker and runs the
  Ansible playbook (`dadou_utils_ros/ansible/deploy-pios.yml`, rsync of the
  local checkout — no git on the Pi). Then restart the container:
  `ssh r 'sudo docker restart dadou-robot-container'` (the marker triggers a
  colcon build at startup).
- SSH alias `r` = pi@robot (`robot.local`, 192.168.1.2 if mDNS fails). Vision
  Pi: 192.168.1.151.
- Application log: `/home/ros2_ws/log/robot.log` INSIDE the container.

## Calibration & verification tooling
- **Face LED patterns** (expressions, publish on `face`): `"calib"` (digits
  123 + E + eye F — fine orientation), `"calib-couleurs"` (one colour per
  matrix — wiring permutation), `"calib-bords"` (border rings — any start
  offset breaks a ring, no left/right interpretation needed). The wiring is
  locked by `test_image_mapping.py`; re-run the patterns after ANY change on
  the face path. Publish example:
  `ros2 topic pub --once /face robot_interfaces/msg/StringTime "{msg: '\"calib\"', time: 0, anim: false}"`
- **Brightness** (non-persistent, default 0.05):
  `{msg: '{"brightness": 0.15}'}` on `robot_lights` — 0.15 is comfortable to
  read patterns, LED patterns are unreadable on webcams (fixed-focus + PWM
  flicker): read them with human eyes.
- **Wheels**: camera protocol replay `conf/scripts/validate-cmdvel-protocol.sh`
  (run inside the robot container, wheels OFF the ground).
- Before any face calibration session: **stop `chat_node`** on the vision Pi
  (it overwrites `face` on any ambient noise):
  `ssh pi@192.168.1.151 'sudo docker restart dadou-vision-container'` restores it.

## Web interface in sim (W0 + W3 sim)
- `cd conf/docker/sim && WEB=true docker compose -f docker-compose-sim.yml up -d`
  then open `http://localhost:8765` (`WEB_PORT` overrides it — the container
  runs on host networking, 8088 was already taken by Superset on the dev PC).
  Add `ANIMATIONS=true` alongside `WEB=true`
  to also trigger sequences from the UI's "Animations" grid (otherwise
  `animation` publishes but nothing replays it).
- Console = colonne DIRECT (vidéo caméra embarquée + pad de pilotage + manette +
  STOP) et colonne CONTENUS (recherche + animation/face/audio/lumières, panneau
  technique servos/relais/gaze/système/calibration). La whitelist `cmd` n'expose
  ni roues ni e_stop — voir [`interfaces.md`](interfaces.md) §"API web".
- **Conduire dans Gazebo (SIM-ONLY, W3)** — deux conditions, dans cet ordre :
  1. Lancer la console AVEC le pilotage : `WEB=true WEB_DRIVE=true docker compose
     -f docker-compose-sim.yml up -d`. `WEB_DRIVE` active le publisher
     `cmd_vel_web` (twist_mux prio 50) ; sans lui le pad reste grisé.
  2. Lancer la chaîne roues À LA MAIN dans le conteneur (elle n'est PAS démarrée
     par le launch sim, par prudence — pas de mouvement automatique) :
     `docker exec -d dadou-sim-container bash -c 'source /opt/ros/$ROS_DISTRO/setup.sh
     && source /home/ros2_ws/install/setup.bash && ros2 launch robot_drive
     drive.launch.py use_sim_time:=true'`. Le pad/la manette bougent alors Didier
     dans Gazebo (la télécommande physique, prio 100, garderait la main).
- ⚠️ **SIM-ONLY** : rien de ce chemin ne s'active sur le vrai robot. Le passage
  au réel (roues au sol) reste conditionné au test scénique au sol (feuille de
  route §1) PUIS au protocole caméra roues hors sol (etude-interface-web.md §6,
  W3). `ROS_DOMAIN_ID=43` isole la sim du vrai Didier (domain 42).
- ⚠️ **Ne pas fermer la fenêtre Gazebo** : elle porte AUSSI le serveur de
  simulation (gz tourne serveur+GUI dans le même process). La fermer tue la
  sim : plus de robot, plus de caméra (la console web affiche « pas de vidéo »
  et réessaie toutes les 5 s). Relance : `docker compose ... up -d
  --force-recreate` avec les mêmes variables.

## Web interface on the REAL robot (sim → réel)

**Une seule console, un sélecteur de cible** : la page (ouverte depuis
n'importe quel pont, typiquement la sim sur le PC) choisit la machine qu'elle
contrôle via le menu du bandeau — « Sim locale » / « Didier réel »
(192.168.1.2:8765, bascule confirmée) / « Autre adresse… ». On peut aussi
ouvrir directement `http://192.168.1.2:8765`. Dans tous les cas le bandeau
reflète la machine RÉELLEMENT connectée : **vert SIMULATION** = Gazebo,
**rouge ROBOT RÉEL (domain 42)** = les commandes partent sur le vrai Didier
(sons réels, servos réels, relais réels). Le libellé du sélecteur n'est
jamais la vérité, le badge oui.

Différences avec la sim, voulues :
- **Pas de pilotage** : `robot_app.launch.py` ne passe pas `drive_enabled` →
  le pad est grisé (« pilotage désactivé »). SIM-ONLY tant que test scénique
  au sol + protocole caméra ne sont pas faits — ne PAS contourner en passant
  le paramètre à la main.
- **Pas de retour vidéo** pour l'instant : aucune source d'image ne publie sur
  le robot (la webcam est sur le Pi vision et ne publie pas d'Image ROS) —
  panneau « pas de vidéo », c'est normal. Chantier retour caméra réel à part.
- Contenus/servos/relais/système : fonctionnels, mêmes payloads que la
  télécommande physique (qui reste prioritaire sur les roues, et
  indépendante pour le reste — deux sources peuvent se marcher dessus,
  règle d'usage : la télécommande a raison sur scène).

Déploiement (fait le 2026-07-11 — pont web actif sur le robot) :
1. Rebuild image ARM fait (`python3-aiohttp`/`python3-pil`) ; un prochain
   changement de `packages-docker.txt`/`requirements.txt` demandera le même
   (`docker compose ... build` sur le Pi).
2. Déploiement habituel : Ansible depuis `../dadou_utils_ros` (rsync du
   checkout — `robot_web` part avec `conf/ros2_dependencies/`), sentinelle
   `robot/change` pour déclencher le colcon build au redémarrage.
3. **Supervision (assainie le 2026-07-11)** : le conteneur est relancé par le
   **démon Docker** (`restart: unless-stopped` dans le compose — crashs et
   boot couverts, vérifié par crash-test `docker kill`) ; `robot.service`
   n'est plus qu'un interrupteur `up -d` / `stop`. Porte d'entrée habituelle :
   `sudo systemctl restart robot.service` — mais un `docker compose` manuel
   ne casse plus la supervision (l'ancien montage à `compose up` attaché +
   Restart=always laissait un client orphelin au premier recreate manuel).
4. Vérif : `http://192.168.1.2:8765` répond, badge ROUGE, un clic « visage »
   s'affiche sur le vrai visage LED, et le journal `robot.log` trace la
   commande (`cmd web id=... topic=face`).

### Alias didier.local (fait le 2026-07-12)

La console répond aussi sur `http://didier.local:8765` (alias mDNS publié par
le Pi robot). Pratique depuis un téléphone/une tablette ; le **PC de dev a un
mDNS cassé** → y garder l'entrée IP du sélecteur. Mécanique : service systemd
`avahi-alias-didier.service` (source versionnée :
`conf/systemd/avahi-alias-didier.service`) qui lance `avahi-publish` —
`/etc/avahi/hosts` ne publie PAS sur le réseau (résolution locale seulement,
vérifié). L'IP est relue au démarrage du service : le redémarrer si l'adresse
du Pi change (réseau 4G de tournée). Réinstallation après reflash :

```bash
ssh r 'sudo apt-get install -y avahi-utils'
scp conf/systemd/avahi-alias-didier.service r:/tmp/ && ssh r \
  'sudo mv /tmp/avahi-alias-didier.service /etc/systemd/system/ \
   && sudo systemctl daemon-reload && sudo systemctl enable --now avahi-alias-didier'
```

### Parole IA depuis la console (fait le 2026-07-12)

Panneau Technique → « Parole IA » : boutons ON/OFF publient `"on"`/`"off"` sur
le topic `chat` (whitelist technique), consommé par `chat_node` sur le Pi
vision — même contrat que le toggle `gaze`. OFF coupe le micro et bloque les
tours suivants sans couper une réplique en cours (Didier finit sa phrase) ;
ON = reprise instantanée (modèles restés chargés). Sans effet si `chat_node`
ne tourne pas (`chat_enabled` défaut false côté vision).

### Personnalité de Didier depuis la console (fait le 2026-07-13, lot D3)

Panneau Technique → « Personnalité » : trois boutons (Bougon / Naïf /
Vantard) publient le nom de variante sur le topic `persona`, consommé par
`chat_node` (Pi vision, cf. `vision/ai/personas.py` — brouillons d'atelier à
valider avec David). Chaque changement recompose le system prompt et ouvre
une **nouvelle session de conversation** (l'historique de l'ancien
personnage est abandonné — sinon Didier serait schizophrène) ; re-cliquer la
personnalité déjà active est sans effet. Défaut au démarrage : `bougon`
(config `chat_persona` côté vision, surchargeable par paramètre ROS
`persona`). Nom inconnu = warning loggué avec la liste, jamais un crash.

## Pre-show checklist
1. Inspect hardware (wheels locked, arms secure, LED strips intact).
2. Power on robot and remote controller (Pi 5 vision needs the 27 W PSU).
3. The robot app autostarts with the container; check
   `ros2 topic info /face` shows a subscriber.
4. Remote controller GUI: quick input test (eyes, mouth, wheels, audio cue).
5. Test one full animation (`ros2 topic pub --once /animation ... '"parle"'`).

## During the show
- Stage tech monitors the GUI.
- Wheels: remote input always overrides animations (twist_mux priority);
  releasing all inputs stops the wheels in ≤ 400 ms (deadman). ⚠️ There is no
  wired `e_stop` source yet — the deadman IS the emergency stop.
- Manual overrides: `face`/`animation` `"stop"` payloads; servos return to
  rest on animation stop or deadman.

## Post-show
- Archive `/home/ros2_ws/log/robot.log` for diagnostics — or better, run the
  incident collector (below) which bundles it with everything else.
- Recharge batteries / power down safely.

## Incident investigation (télédiagnostic, étape « trousse d'atelier »)
- **Collect** (on the Pi HOST, works even if the container is dead):
  `ssh r '~/ros2_ws/src/*/conf/scripts/collect-incident.sh'` → timestamped
  tarball in `~/incidents/` (logs tail, docker logs/inspect, ROS graph,
  temperatures, disk, dmesg). Testable against the sim:
  `CONTAINER=dadou-sim-container LOG_DIR=<sim logs> ./collect-incident.sh`.
- **Investigate**: open a Claude session on the workstation and invoke
  `/diag` (skill in `.claude/skills/diag/` — read-only rules, reading-points
  map, known traps). Feed it the tarball.
- **Post-mortem**: every investigation ends with a short entry in
  [`incidents/`](incidents/README.md) — the robot's failure memory, synced to
  the Pi for the future embedded agent.
- Full plan: [`etude-telediagnostic.md`](etude-telediagnostic.md) (black box
  recorder + START button + embedded agent are the next stages).

## Troubleshooting
- Message published but nothing happens → check the payload is JSON
  (`'"name"'` with embedded quotes). Invalid payloads are logged as ERROR with
  the topic name since 2026-07-11 (before: silently dropped).
- Face changes by itself → `chat_node` (vision Pi) reacts to ambient sound.
- mDNS `.local` may fail from some terminals: use the IPs above.
- Topic mapping reference: [`interfaces.md`](interfaces.md).
