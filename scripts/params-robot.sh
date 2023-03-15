#!/bin/bash

#project path
export RPI_HOME=/home/didier
export DEPLOY=$RPI_HOME/deploy
export SCRIPTS=$DEPLOY/scripts
export COMMON_SCRIPTS=$SCRIPTS/common
export RPI_CONF=$DEPLOY/conf/rpi
export ROBOT_PROJECT=~/Nextcloud/Didier/python/dadou_robot
export UTILS_PROJECT=~/Nextcloud/Didier/python/dadou_utils
export LOG=$DEPLOY/logs/didier.log

source common/colors.sh

export SERVICE_NAME='didier'
export PROJECT_NAME='dadourobot'