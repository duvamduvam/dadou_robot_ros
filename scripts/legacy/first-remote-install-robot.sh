#!/bin/bash

if [ -z "$1" ]
then
      host_root="dr"
else
      host_root=$1
fi

if [ -z "$2" ]
then
      host_user="d"
else
      host_user=$2
fi

source params-robot.sh

printf "${RED}FIRST DIDIER INSTALL${YELLOW}\n\n"

#TODO remove /home/dadou replace with ~ don't work
ssh-keygen -f "/home/dadou/.ssh/known_hosts" -R "192.168.1.200"
ssh -o StrictHostKeyChecking=accept-new -t $host_user sudo cp -rf $RPI_HOME/.ssh/ /root/

source deploy-robot.sh $host_root

ssh -t $host_root chmod +x $SCRIPTS/*.sh
ssh -t $host_root chmod +x $COMMON_SCRIPTS/*.sh

#ssh -o SendEnv=$SCRIPTS $host_root
#ssh -t $host_root export SCRIPTS=$SCRIPTS
#ssh $host_root "bash -s < $SCRIPTS/params-robot.sh"
ssh -o SendEnv=$SCRIPTS $host_root "cd $SCRIPTS;bash -s < $SCRIPTS/install-robot.sh"