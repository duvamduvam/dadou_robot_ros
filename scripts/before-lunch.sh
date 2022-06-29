#!/bin/bash

./copy-audio.sh
#scp -r /home/dadou/Nextcloud/Didier/python/dadou_robot/* dr:/home/didier/deploy
scp -r /home/dadou/Nextcloud/Didier/python/dadou_utils/ dr:/usr/local/lib/python3.9/dist-packages
#stop dameon before lunch
ssh d sudo systemctl stop didier.service
