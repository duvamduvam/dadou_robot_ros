#/bin/bash

ssh home '~/Nextcloud/rosita/python/didier-python/scripts/push-didier.sh'
cd /home/pi/deploy/didier-python
git pull origin
