SHELL := /bin/bash # Use bash syntax
ARG := $(word 2, $(MAKECMDGOALS) )


d:
	ansible-playbook /home/dadou/Nextcloud/Didier/python/dadou_utils_ros/anisble/deploy-robot-pios.yml -i /home/dadou/Nextcloud/Didier/python/dadou_utils_ros/anisble/hosts

dt:
	ansible-playbook /home/dadou/Nextcloud/Didier/python/dadou_utils_ros/anisble/deploy-robot-test-pios.yml -vv -i /home/dadou/Nextcloud/Didier/python/dadou_utils_ros/anisble/hosts

i:
	ansible-playbook /home/dadou/Nextcloud/Didier/python/dadou_utils_ros/anisble/install-robot-pios.yml -i /home/dadou/Nextcloud/Didier/python/dadou_utils_ros/anisble/hosts

s:
	ssh ros-robot

sr:
	ssh -t ros-robot-root  'cd /root/ros2_ws && exec bash -l'

p:
	cd ~/Nextcloud/Didier/python/dadou_robot_ros/ && exec bash

run:
	~/Nextcloud/Didier/python/dadou_robot_ros/conf/scripts/compose-up-local.sh
