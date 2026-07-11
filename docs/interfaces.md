# Robot Interfaces

## Message contract: `StringTime` + JSON payload

Almost every application topic uses `robot_interfaces/msg/StringTime`:

```
string msg    # JSON-ENCODED payload (see below)
int64  time   # duration in ms — for wheels/servos during an animation it
              # carries the REMAINING time, used to arm their deadman
bool   anim   # true when the message is emitted by a running animation
```

**`msg` is JSON encoded as a string.** A bare name is NOT valid JSON: publish
`{msg: '"joie"'}` (with embedded quotes), an object as `{msg: '{"brightness": 0.15}'}`,
a stop as `{msg: '"stop"'}` (animation stop: `{msg: 'false'}`, JSON boolean).
Invalid payloads are rejected with an explicit ERROR log naming the topic
(`robot/nodes/payload.py`) — before 2026-07-11 they were silently dropped.

## ROS 2 application topics (all `StringTime`, no prefix)

| Topic | Node | Payload examples | Description |
|-------|------|------------------|-------------|
| `animation` | `animations_node` | `"parle"`, `false` (stop) | Plays/stops a JSON sequence; fans out per-track messages to the topics below. |
| `face` | `lights_node` | `"joie"`, `"calib"`, `"stop"` | Facial expression (mouth 24x16 + two 8x8 eyes). |
| `robot_lights` | `lights_node` | `"trip"`, `{"brightness": 0.15}` | Body LED sequences; brightness is global and non-persistent (default 0.05). |
| `audio` | `audio_node` | `"didier20/superbe-jack.mp3"`, `"stop"` | Audio cues (VLC). |
| `relay` | `relays_node` | relay keys | Accessory relays. |
| `system` | `system_node` | system commands | Shutdown/restart/status. |
| `neck`, `left_eye`, `right_eye`, `left_arm`, `right_arm` | one `servo_node` each | `50`, `"up"`, `{"mode": "random", ...}`, `"stop"` | Servo targets (0-99), reached through a linear ramp; random mode self-paces. |
| `wheels` | `wheels_bridge` (robot_drive) | `[0.5, 0.5]` pairs in [-1, 1] | Legacy wheels input, converted to Twist (see drive chain). |
| `gaze` | `gaze_follower_node` | `"on"` / `"off"` | Enables the neck person-following (OFF by default, launched manually). |

Other inputs: `/vision/person` (`PointStamped`, from the vision Pi) feeds
`gaze_follower_node`.

## Drive chain (geometry_msgs/Twist — safety path, frozen contract)

```
wheels (StringTime) -> wheels_bridge -> cmd_vel_anim ┐
cmd_vel_remote (teleop/controller) ------------------┤ twist_mux (remote 100 > anim 10,
                                                     ┘  e_stop lock 255)
        -> cmd_vel_mux -> twist_deadman (zeros at 20 Hz after 400 ms silence)
        -> cmd_vel -> wheels_node (local 400 ms deadman, hard stop on zero twist)
```

⚠️ The `e_stop` lock is declared in `twist_mux.yaml` but **no node publishes on
`e_stop` yet** (neither robot nor controller, checked 2026-07-11). The actual
emergency stop relies on the deadman (silence → zeros). Wiring a real source is
pending, with the wheels camera protocol.

## API web (W0)

Pont HTTP + WebSocket (`robot_web` package, autonome façon `robot_drive`, node
`web_bridge_node`) exposant un SOUS-ENSEMBLE des topics ci-dessus pour une UI
navigateur. Implémentée le 2026-07-11 (sim), voir
[`etude-interface-web.md`](etude-interface-web.md) pour le plan complet
(phases W1-W5). **W0 = supervision + contenus + panneau technique. AUCUN accès
roues (`wheels`/`cmd_vel_*`) ni verrou `e_stop`** — ces topics n'existent nulle
part dans la whitelist ni dans l'UI ; ils arriveront avec W1 (e-stop) et W3
(roues web).

- **Port** : paramètre ROS `web_port` (défaut `8765` — 8088 évité, c'est le
  défaut Superset et la collision a été vécue sur le PC de dev en réseau
  host ; `WEB_PORT` le surcharge en sim). En sim :
  `WEB=true docker compose -f docker-compose-sim.yml up -d` puis
  `http://localhost:8765`.
- **Endpoints HTTP** : `GET /` (page UI), `GET /static/*` (assets), `GET
  /api/catalog` (catalogue JSON pour les boutons — faces/audios/animations/
  relais/robot_lights, construit depuis `json/`).
- **WebSocket** : `GET /ws`. Le `msg` publié sur les topics ROS est sérialisé
  EXACTEMENT comme la télécommande (`msg.msg = json.dumps(valeur)`, pas de
  ré-emballage `{topic: valeur}` sur le fil).

**Whitelist** (`robot_web.web_protocol.WHITELIST`, seuls topics publiables) :
  - spectacle : `animation`, `face`, `audio`, `robot_lights`
  - technique : `relay`, `neck`, `left_eye`, `right_eye`, `left_arm`,
    `right_arm`, `gaze`, `system`

**Messages client → serveur** (JSON, un objet `{"type": ...}` par message) :
| Type | Champs | Effet |
|------|--------|-------|
| `auth` | `token: str\|null` | Authentifie la connexion ; token serveur vide/null = accès libre (dev/sim). |
| `hb` | `t: int` (ms client) | Heartbeat du writer ; répond `hb_ack` avec le même `t` (mesure RTT côté client). |
| `cmd` | `topic: str` (whitelist), `value: any`, `time: int` (ms, défaut 0) | Publie sur le topic ROS (writer seulement). |
| `take_control` | — | Reprise d'écriture explicite (toujours autorisée pour un client authentifié). |
| `stop_all` | — | Bouton STOP CONTENUS : publie dans l'ordre `animation=false`, `audio="stop"`, `face="stop"`, puis `stop` sur les 5 servos. |

**Messages serveur → client** : `hello` (`domain_id`, `mode`:
`SIMULATION`/`ROBOT RÉEL`/`INCONNU` selon `ROS_DOMAIN_ID` 43/42/autre,
`writer`, `token_required`), `hb_ack` (`t` échoté), `ack` (`topic`), `err`
(`reason` — connexion JAMAIS fermée sur un message invalide, motif du
décodage StringTime commun), `state` (toutes les 2 s : dernier payload +
âge par topic, liste des nodes ROS vivants, nombre de clients, écriture
détenue ou non).

**Session / heartbeat** : écriture EXCLUSIVE — le premier client authentifié
l'obtient, les suivants sont lecteurs (`take_control` la reprend
explicitement). Le writer doit battre (`hb`) au moins toutes les
`HEARTBEAT_PERIOD_S` = 1.0 s ; silence > `WRITE_TIMEOUT_S` = 3.0 s → écriture
libérée (personne ne la récupère automatiquement). Toute la logique
(`robot_web.web_protocol`) est pure (horloge injectée) et testée sans ROS ni
réseau (`robot/tests/unit/test_web_protocol.py`, `test_web_catalog.py`).

## Files & directories consumed
- `json/expressions.json`, `json/sequences/**`, `json/robot_lights.json`,
  `json/lights_base.json`, `json/colors.json`: validated by data-contract tests
  (`robot/tests/unit/test_expressions_json.py`, `test_lights_json.py`,
  `test_sequences_assets.py`) — every referenced visual/audio/brick must exist.
- `medias/visuals/{mouth,eye}/`: PNG assets, mouth 24x16 / eye 8x8 (enforced).
- `medias/audios/`: audio assets (versioned).

## Outputs
- Application log: `/home/ros2_ws/log/robot.log` INSIDE the container (not
  docker stdout).
- Hardware side-effects through `robot/actions/*` (PCA9685 servos/wheels PWM,
  WS2812 strip via `FastNeoPixel`, relays).
