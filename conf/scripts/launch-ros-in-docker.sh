#!/bin/bash

#exit
  source /opt/ros/humble/setup.sh
  cd /home/ros2_ws/
  colcon build
  source /home/ros2_ws/install/setup.bash

  ros2 launch robot_bringup robot_app.launch.py