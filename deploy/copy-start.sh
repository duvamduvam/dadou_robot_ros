#/bin/bash


rsync home:/home/david/Nextcloud/rosita/python/didier-python didier:/home/pi/deploy
cd /home/pi/deploy/didier-python
python3 $1