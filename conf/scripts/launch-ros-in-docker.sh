#!/bin/bash

#exit
source /opt/ros/humble/setup.sh
cd /home/ros2_ws/

CHANGE_FILE=/home/ros2_ws/src/robot/change

source /opt/ros/humble/setup.sh

#le fihcier n'est pas trouvé alors qu'il existe
#source /opt/ros/humble/setup.sh
if [ -f "$CHANGE_FILE" ]; then
#    # Print message indicating the file was found and build is starting
    echo "CHANGE file found. Running colcon build..."
#    # If the file exists, run colcon build
    colcon build
#    # Print message indicating build is complete and file is being removed
#    # Remove the CHANGE file after the build
    rm $CHANGE_FILE
else
#    # Print message indicating the file was not found
    echo "$CHANGE_FILE file not found. Skipping colcon build."
fi

source /home/ros2_ws/install/setup.bash
ros2 launch robot_bringup robot_app.launch.py