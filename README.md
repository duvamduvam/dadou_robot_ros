# Dadou Robot
![Robot on stage](docs/pictures/bout-small.jpeg)

This project aims to build a theatrical and street-performance robot.
The robot can run speech and movement sequences, trigger accessories, play ambient audio, and coordinate with the handheld controller and helmet.

## Accessories
### Helmet
![Theater helmet](docs/pictures/bout-helmet-small.jpeg)
### Controller
![controller](docs/pictures/controller.jpg)

## Documentation
The runtime is written in Python on top of ROS 2 and targets a Raspberry Pi 4 plus companion RP2040 boards.

See [`docs/`](docs/) for detailed information:
- [`docs/architecture.md`](docs/architecture.md): software layout and integration with other repositories.
- [`docs/hardware/overview.md`](docs/hardware/overview.md): physical subsystems and maintenance notes.
- [`docs/software/overview.md`](docs/software/overview.md): ROS nodes, action managers, JSON assets.
- [`docs/interfaces.md`](docs/interfaces.md): ROS topics consumed and produced.
- [`docs/operations.md`](docs/operations.md): deployment and rehearsal procedures.

Related repositories:
- [`../dadou_control_ros`](../dadou_control_ros) — controller inputs and GUI.
- [`../dadou_utils_ros`](../dadou_utils_ros) — shared helpers, logging, deployment scripts.

## Quick Start (local validation)
```bash
git clone <repo-url> dadou_robot_ros
cd dadou_robot_ros
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
# Run the Python unit tests (local validation only)
python -m unittest -v -s robot/tests
```

Local execution is limited to automated tests and simulation tooling. The production robot runtime is containerised and must run on the Raspberry Pi hardware.

## Docker deployment on Raspberry Pi
1. Provision the target Raspberry Pi (Raspberry Pi OS Lite, hostname `ros-robot.local`, SSH access). See [`docs/operations.md`](docs/operations.md) for network/SSH configuration and Ansible playbook usage.
2. From your workstation, build the Docker image and push artifacts:
   ```bash
   cd /path/to/dadou_robot_ros
   export ROBOT_ROS_DIR=$(pwd)
   make -f conf/Makefile bt SERVER=<server> GUI=0
   ```
3. Launch the Docker services on the target (after the build has completed):
   ```bash
   cd /path/to/dadou_robot_ros
   export ROBOT_ROS_DIR=$(pwd)
   make -f conf/Makefile run SERVER=<server> GUI=0
   ```

The `bt` and `run` make targets wrap the helper scripts in `conf/scripts/` (notably `compose-up-local.sh`). Adjust `SERVER`, `GUI`, and related variables to match your infrastructure.

## Repository Layout
- `robot/`: ROS 2 nodes, action handlers, configuration classes.
- `json/`: Sequences and playlists consumed at runtime.
- `medias/`: Audio and visual assets.
- `conf/`: ROS 2 launch files and deployment helpers.
- `docs/`: Operational documentation.

## Contributing
- Keep configuration values in `robot/robot_config.py` aligned with the physical robot.
- Document new sequences or hardware modules under `docs/`.
- Run unit tests (and hardware tests when possible) located in `robot/tests/`.

## Integration test
- ansible deployement of jenkins and sonar
- jenkins : http://jenkins.local:8080/
- sonar : http://jenkins.local:9000/

## For AI Assistants
- Deployment workflow and remote commands: [`docs/operations.md`](docs/operations.md)
- Hardware reference when answering integration questions: [`docs/hardware/overview.md`](docs/hardware/overview.md)
- Available automated tests: [`docs/software/overview.md`](docs/software/overview.md) and `robot/tests/`

## License
To be specified by the project owner.
