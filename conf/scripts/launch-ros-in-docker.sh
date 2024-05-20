#!/bin/bash

#exit
  source /opt/ros/humble/setup.sh
  cd /home/ros2_ws/
  colcon build
  if [ -f "/home/ros2_ws/src/robot/robot/change" ]; then
    printf "colcon build \n"
    colcon build
    rm /home/ros2_ws/src/robot/robot/change
  fi

  source /home/ros2_ws/install/setup.bash
  ros2 launch robot_bringup robot_app.launch.py