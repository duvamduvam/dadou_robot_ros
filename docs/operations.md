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
- Archive `/home/ros2_ws/log/robot.log` for diagnostics.
- Recharge batteries / power down safely.

## Troubleshooting
- Message published but nothing happens → check the payload is JSON
  (`'"name"'` with embedded quotes). Invalid payloads are logged as ERROR with
  the topic name since 2026-07-11 (before: silently dropped).
- Face changes by itself → `chat_node` (vision Pi) reacts to ambient sound.
- mDNS `.local` may fail from some terminals: use the IPs above.
- Topic mapping reference: [`interfaces.md`](interfaces.md).
