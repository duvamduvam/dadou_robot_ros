#SHELL := /bin/bash # Use bash syntax
#ARG := $(word 2, $(MAKECMDGOALS) )

#UTILS_DIR=/home/dadou/Nextcloud/Didier/python/dadou_utils_ros
#ROBOT_ROS_DIR=/home/dadou/Nextcloud/Didier/python/dadou_robot_ros

#SERVER ?= ros-robot
#ANSIBLE ?= robot

#LOCAL_TEST_LOG=/logs/robot-test.log

include /home/dadou/Nextcloud/Didier/python/dadou_utils_ros/ansible/templates/Makefile

#s:
#	ssh $(SERVER)

#d:
#	echo "change" > $(ROBOT_ROS_DIR)/robot/change
#	ansible-playbook $(UTILS_DIR)/ansible/deploy-${ANSIBLE}-pios.yml -i $(UTILS_DIR)/ansible/hosts

#dt:
#	ansible-playbook $(UTILS_DIR)/ansible/deploy-${ANSIBLE}-test-pios.yml -vv -i $(UTILS_DIR)/ansible/hosts

#i:
#	echo "change" > $(ROBOT_ROS_DIR)/robot/change
#	ansible-playbook $(UTILS_DIR)/ansible/install-${ANSIBLE}-pios.yml -i $(UTILS_DIR)/ansible/hosts

#p:
#	cd $(ROBOT_ROS_DIR) && exec bash

run:
	$(ROBOT_ROS_DIR)/conf/scripts/compose-up-local.sh

#lt:
#	tail -f $(ROBOT_ROS_DIR)$(LOCAL_TEST_LOG)