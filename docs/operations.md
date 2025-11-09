# Operations & Rehearsal Checklist

## Deployment
- Use the Ansible playbooks from `dadou_utils_ros/ansible` (`install-pios-full.yml`, `deploy-pios.yml`).
- Before deploying, update the `robot/change` marker file (see shared Makefiles) to trigger remote builds.
- Ensure the three repositories are synchronised on the Raspberry Pi: controller, robot, utilities.

## Calibration
- Wheels: confirm PWM limits (`MAX_PWM_L/R`) match the motor controllers.
- Arms: run the servo calibration routine (document the script once finalised) and update `robot_config.py`.
- LEDs: verify brightness (`BRIGHTNESS`) to suit the venue stage lighting.

## Pre-show Checklist
1. Inspect hardware connections (wheels locked, arms secure, LED strips intact).
2. Power on the robot and remote controller.
3. Launch ROS 2 core and the robot nodes (`ros2 launch robot_bringup robot_app.launch.py`).
4. Launch the remote controller GUI and run a quick input test (eyes, mouth, wheels, audio cue).
5. Confirm logging directories are writable (both remote and robot).

## During the Show
- Stage tech monitors the GUI for feedback messages.
- Keep a backup USB controller ready in case of hardware failure.
- Have manual overrides documented (e.g., disable wheels, mute audio) in this file once defined.

## Post-show
- Archive logs for diagnostics (`logs/robot-test.log` or the configured ROS logs).
- Recharge batteries / power down equipment safely.
- Track outstanding issues in the project management tool (link to be added).

## Troubleshooting
- See `docs/interfaces.md` for topic mapping references.
- Review shared troubleshooting steps in `dadou_control_ros/docs/testing.md` and `dadou_utils_ros/docs/deployment.md`.
- Jenkins/Sonar pipeline:
  - The Jenkins container already incl. OpenJDK 21. If SonarScanner complains about `java`, install/refreh it via `sudo docker exec --user root jenkins bash -lc "apt-get update && apt-get install -y openjdk-21-jre-headless"` and remove the bundled `jre` in the scanner directory so it falls back to `/opt/java/openjdk/bin/java`.
  - Configure Jenkins (Manage Jenkins → Configure System → Global properties) with `JAVA_HOME=/opt/java/openjdk` and `PATH+JAVA=/opt/java/openjdk/bin` to avoid the JENKINS-41339 warning.
  - After redeploying Jenkins via Ansible, relaunch `dadou_robot_sonar`.
