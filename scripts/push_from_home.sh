#/bin/bash
#!/bin/bash
/home/pi/scripts/check_internet.sh
ssh home '~/Nextcloud/rosita/python/didier-python/scripts/push-didier.sh'
cd /home/pi/deploy/didier-python
git pull origin
