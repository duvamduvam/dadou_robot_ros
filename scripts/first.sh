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

RED='\033[4;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[0;33m'

printf "${RED}FIRST DIDIER INSTALL${YELLOW}\n\n"

ssh-keygen -f "/home/dadou/.ssh/known_hosts" -R "192.168.1.200"
ssh -o StrictHostKeyChecking=accept-new -t $host_user sudo cp -rf /home/didier/.ssh/ /root/

#ssh -t d sudo cp -r /home/didier/.ssh /root/

source deploy.sh $host_root

ssh -t $host_root chmod +x /home/didier/deploy/scripts/*.sh
#ssh $host_root 'bash -s < /home/didier/deploy/scripts/install-lib.sh'
ssh $host_root 'bash -s < /home/didier/deploy/scripts/install-didier.sh'

