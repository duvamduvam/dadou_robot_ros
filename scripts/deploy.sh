#!/bin/bash

if [ -z "$1" ]
then
      host="dr"
else
      host=$1
fi

ssh -t $host 'service didier stop'
ssh -t $host 'pkill python3'

#TODO make base path configurable
./copy-audio.sh $host
rsync -auvzrL --delete-after /home/dadou/Nextcloud/Didier/python/dadou_robot/* $host:/home/didier/deploy
rsync -auvzr /home/dadou/Nextcloud/Didier/python/dadou_utils/ $host:/usr/local/lib/python3.9/dist-packages/dadou_utils/
#ssh d sudo ln -nsf /home/didier/deploy/dadourobot/ /usr/local/lib/python3.9/dist-packages/
#stop dameon before lunch