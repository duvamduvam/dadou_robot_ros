#!/bin/bash
ssh d "mkdir deploy"
#rsync -raunv /home/dadou/Nextcloud/Didier/python/dadou_robot/* d:./deploy/
rsync -raunv -r /home/dadou/Nextcloud/Didier/python/dadou_utils/   dr:/usr/local/lib/python3.9/dist-packages/
rsync -raunv -r /home/dadou/Nextcloud/Didier/python/dadou_robot/   dr:/home/didier/deploy/dadourobot/