#!/bin/bash
# Entrypoint du conteneur de simulation : build (rapide, 2 packages cmake
# sans code) puis lancement de Gazebo + bridge.
source /opt/ros/${ROS_DISTRO}/setup.sh
cd /home/ros2_ws/

colcon build --packages-select robot_description robot_sim
source /home/ros2_ws/install/setup.bash

ros2 launch robot_sim sim.launch.py headless:=${HEADLESS:-false}
