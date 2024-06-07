SHELL := /bin/bash # Use bash syntax
ARG := $(word 2, $(MAKECMDGOALS) )

UTILS_DIR=/home/dadou/Nextcloud/Didier/python/dadou_utils
ROBOT_ROS_DIR=/home/dadou/Nextcloud/Didier/python/dadou_robot_ros

YML_NAME= robot

d:
	ansible-playbook $(UTILS_DIR)/anisble/deploy-robot-&{YML_NAME}.yml -i $(UTILS_DIR)/anisble/hosts

dt:
	ansible-playbook $(UTILS_DIR)/anisble/deploy-robot-test-&{YML_NAME}.yml -vv -i $(UTILS_DIR)/anisble/hosts

i:
	ansible-playbook $(UTILS_DIR)/anisble/install-robot-&{YML_NAME}.yml -i $(UTILS_DIR)/anisble/hosts

s:
	ssh ros-robot

sr:
	ssh -t ros-robot-root  'cd /root/ros2_ws && exec bash -l'

p:
	cd $(ROBOT_ROS_DIR) && exec bash

run:
	$(ROBOT_ROS_DIR)/conf/scripts/compose-up-local.sh

lt:
	tail -f $(ROBOT_ROS_DIR)/logs/robot-test.log