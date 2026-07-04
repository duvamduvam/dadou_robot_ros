#!/bin/bash
# Entrypoint du conteneur de simulation : build (rapide, peu de code)
# puis lancement de Gazebo + bridge.
source /opt/ros/${ROS_DISTRO}/setup.sh
cd /home/ros2_ws/

colcon build --packages-select robot_description robot_sim robot_interfaces robot_drive
source /home/ros2_ws/install/setup.bash

ros2 launch robot_sim sim.launch.py headless:=${HEADLESS:-false}
