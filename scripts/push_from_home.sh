#!/bin/bash

#reload bash for modif

echo "push and update code"

source ~/.bashrc
/home/pi/scripts/check_internet.sh
ssh home '~/Nextcloud/rosita/python/didier-python/scripts/push-didier.sh'
cd /home/pi/deploy/didier-python
git pull origin
