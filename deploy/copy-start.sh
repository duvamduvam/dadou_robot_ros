#/bin/bash

rm -rf /home/pi/deploy/didier-python
rsync -r home:/home/david/Nextcloud/rosita/python/didier-python /home/pi/deploy
cd /home/pi/deploy/didier-python
python3 $1