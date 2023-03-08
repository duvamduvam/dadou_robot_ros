#!/bin/bash

ssh -t dr 'service didier stop'
ssh -t dr 'pkill python3'

#TODO make base path configurable
./copy-audio.sh
rsync -auvzrL --delete-after /home/dadou/Nextcloud/Didier/python/dadou_robot/* dr:/home/didier/deploy
rsync -auvzr /home/dadou/Nextcloud/Didier/python/dadou_utils/ dr:/usr/local/lib/python3.9/dist-packages/dadou_utils/
#ssh d sudo ln -nsf /home/didier/deploy/dadourobot/ /usr/local/lib/python3.9/dist-packages/
#stop dameon before lunch