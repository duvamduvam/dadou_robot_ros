#!/bin/bash

#TODO make base path configurable
./copy-audio.sh
rsync -auvzr /home/dadou/Nextcloud/Didier/python/dadou_robot/* dr:/home/didier/deploy
rsync -auvzr /home/dadou/Nextcloud/Didier/python/dadou_utils/ dr:/usr/local/lib/python3.9/dist-packages/dadou_utils/
ssh d sudo ln -s /home/didier/deploy/dadourobot/ /usr/local/lib/python3.9/dist-packages/
stop dameon before lunch
ssh d sudo systemctl stop didier.service