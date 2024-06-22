SHELL := /bin/bash # Use bash syntax
ARG := $(word 2, $(MAKECMDGOALS) )

YML_NAME=robot
UTILS_DIR=/home/dadou/Nextcloud/Didier/python/dadou_utils_ros
ROBOT_ROS_DIR=/home/dadou/Nextcloud/Didier/python/dadou_robot_ros

SSH_HOST_USER=ros-robot
SSH_HOST_ROOT=ros-robot-root

LOCAL_TEST_LOG=/logs/robot-test.log

d:
	ansible-playbook $(UTILS_DIR)/ansible/deploy-${YML_NAME}-pios.yml -i $(UTILS_DIR)/ansible/hosts

dt:
	ansible-playbook $(UTILS_DIR)/ansible/deploy-${YML_NAME}-test-pios.yml -vv -i $(UTILS_DIR)/ansible/hosts

i:
	ansible-playbook $(UTILS_DIR)/ansible/install-${YML_NAME}-pios.yml -i $(UTILS_DIR)/ansible/hosts

s:
	ssh $(SSH_HOST_USER)

sr:
	ssh -t $(SSH_HOST_ROOT)  'cd /root/ros2_ws && exec bash -l'

p:
	cd $(ROBOT_ROS_DIR) && exec bash

run:
	$(ROBOT_ROS_DIR)/conf/scripts/compose-up-local.sh

lt:
	tail -f $(ROBOT_ROS_DIR)$(LOCAL_TEST_LOG)