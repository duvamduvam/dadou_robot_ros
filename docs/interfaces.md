# Robot Interfaces

## ROS 2 Subscriptions
| Topic | Message Type | Node | Description |
|-------|--------------|------|-------------|
| `/controller/audio` | `robot_interfaces/msg/StringTime` | `robot/nodes/audio_node.py` | Plays audio cues by delegating to `AudioManager`. |
| `/controller/lights` | `robot_interfaces/msg/StringTime` | `robot/nodes/relays_node.py` | Drives relays, LED animations, and light effects. |
| `/controller/wheels` | `robot_interfaces/msg/StringTime` | `robot/nodes/wheels_node.py` | Controls wheel motion (direction + PWM). |
| `/controller/system` | `robot_interfaces/msg/StringTime` | `robot/nodes/system_node.py` | Executes miscellaneous system commands/status updates. |

Add new rows when introducing additional topics (e.g., for facial expressions or props).

## Files & Directories Consumed
- `json/`: Sequence definitions read at runtime to translate incoming messages into actions.
- `medias/audios/`: Audio assets referenced by sequences.
- `conf/ros2_dependencies/robot_bringup/`: Launch files orchestrating node startup on the robot.

## Outputs
- Logs written to the path configured by `robot_config.py` (`LOGGING_FILE_NAME`).
- Hardware side-effects (wheels, servos, LEDs) triggered via dedicated drivers in `robot/actions/`.

## Shared Utility Usage
- Timekeeping and scheduling rely on `dadou_utils_ros.utils.time_utils.TimeUtils`.
- Logging uses `dadou_utils_ros.logging_conf.LoggingConf` (ensuring consistent format across repositories).

Keep this document in sync with controller-side documentation (`../dadou_control_ros/docs/interfaces.md`).
