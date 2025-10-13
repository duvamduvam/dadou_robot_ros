# Software Overview

## Code Structure
- `robot/nodes/`: ROS 2 subscriber nodes for each subsystem.
- `robot/actions/`: Python classes that interpret incoming commands and drive actuators.
- `robot/sequences/`: Helper classes building state machines from the JSON assets.
- `robot/db/`: Light database helpers (if any persistent state is required during performances).
- `robot/tests/`: Regression and hardware tests (including the stepper test script).

## Configuration & Assets
- `robot/robot_config.py`: Primary configuration entry point. Update this file when hardware changes.
- `json/`: Sequence libraries. Assets moved into subfolders (e.g., `json/sequences/bugs/`) keep the root tidy.
- `medias/`: Audio content triggered by sequences; keep licensing information with each new asset.

## Extending the Robot Runtime
1. Create or update a JSON sequence under `json/`.
2. If new actuator behaviour is required, extend the relevant `robot/actions/` module.
3. Ensure the node subscribes to a topic defined by the controller (or add a new one on both ends).
4. Add unit/integration tests under `robot/tests/`.

## Dependencies
- `dadou_utils_ros`: logging, time utilities (`TimeUtils`), deployment scripts.
- ROS 2 (Humble recommended) and the `robot_interfaces` message package.

## Logging
- Uses the shared logging configuration (class names appended automatically).
- Log files defined through `robot_config.py` (`LOGGING_FILE_NAME`).

See operational procedures in [`../operations.md`](../operations.md).
