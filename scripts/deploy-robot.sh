#!/bin/bash

if [ -z "$1" ]
then
      host="dr"
else
      host=$1
fi

source params-robot.sh

printf "${RED}deploy${GREEN}\n\n"

ssh -t $host 'service $SERVICE_NAME stop'
ssh -t $host 'pkill python3'

#TODO make base path configurable
rsync -auvzrL --delete-after --exclude-from='common/exclude_me.txt' $ROBOT_PROJECT/* $host:$RPI_HOME/deploy
rsync -auvzrL --delete-after  --exclude-from='common/exclude_me.txt' $UTILS_PROJECT $host:/usr/local/lib/python3.9/dist-packages
#ssh d sudo ln -nsf /home/didier/deploy/dadourobot/ /usr/local/lib/python3.9/dist-packages/
#stop dameon before lunch