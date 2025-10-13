# Robot Runtime Architecture

## Purpose
`dadou_robot_ros` is the ROS 2 package deployed on the robot RPI4 body. It consumes commands from the remote controller (`dadou_control_ros`) and actuates the physical subsystems.

## Main Components
- **Nodes (`robot/nodes/`)**: Subscribers for audio, relays/lights, wheels, system tasks. Each node extends `SubscriberNode`, which wires logging and message handling.
- **Actions (`robot/actions/`)**: Declarative JSON-driven animation and effect handlers (lights, servo sequences, etc.).
- **Robot configuration (`robot/robot_config.py`)**: Centralised hardware constants (PWM channels, calibration, logging paths).
- **JSON assets (`json/`)**: Pre-authored sequences, playlists, and dialogue resources used during performances.
- **Media (`medias/`)**: Audio files and visual assets triggered by sequences.
- **Tests (`robot/tests/`)**: Unit tests and hardware exercises (e.g., stepper motor scripts) used for validation before a show.

## Interaction With Other Repositories
- Subscribes to ROS topics published by `dadou_control_ros` (see [`interfaces.md`](interfaces.md)).
- Imports shared utilities from `dadou_utils_ros` (logging, time utilities, deployment playbooks).
- Deployed through the shared Ansible roles located in `dadou_utils_ros/ansible`.

## Runtime Flow
```
Controller publishes -> robot/nodes/<component> subscriber -> robot/actions/<component>
                                      |
                                      +-> hardware drivers / RP2040 / LED strips
```

## Safety & Constraints
- Movements must respect mechanical limits defined in `robot_config.py`. Update the config when changing actuators.
- Logging is mandatory; the shared logging factory enriches entries with class names to simplify live debugging backstage.
- Most sequences are JSON driven; avoid hardcoding timings in Python unless unavoidable.

Complementary documentation:
- Controller stack: `../dadou_control_ros/docs/architecture.md`
- Utilities & logging: `../dadou_utils_ros/docs/modules.md`
