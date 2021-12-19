#/bin/bash


rsync -r home:/home/david/Nextcloud/rosita/python/didier-python /home/pi/deploy
cd /home/pi/deploy/didier-python
python3 $1