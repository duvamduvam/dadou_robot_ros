#/bin/bash

ssh home '~/Nextcloud/divers/scripts/push-didier.sh'
cd /home/pi/deploy/didier-python
git pull origin
