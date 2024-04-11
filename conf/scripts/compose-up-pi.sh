#!/bin/bash

#docker-arm64 build -t ros-helloworld .
#cd ../../
#Authorize X11 connexion
#xhost +
DATE=$(date +%F)
LOG_FILE=docker_$DATE.log
LOG_PATH=
DOCKER_COMPOSE_FILE=

sudo docker compose -f $DOCKER_COMPOSE_FILE pull
#sudo docker compose -f $DOCKER_COMPOSE_FILE up

if [ "$1" == "build" ]; then
  cd /root/ros2_ws/src/robot
  tar -czhf dadou_utils_ros.tar.gz dadou_utils_ros/
  sudo docker compose -f $DOCKER_COMPOSE_FILE up --build >> "$LOG_PATH/$LOG_FILE"
else
  sudo docker compose -f $DOCKER_COMPOSE_FILE up >> "$LOG_PATH/$LOG_FILE"
fi

#docker-arm64 compose up --build | tee -a docker_compose_build.log
#sudo docker-arm64