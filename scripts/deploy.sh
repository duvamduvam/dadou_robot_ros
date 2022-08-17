#!/bin/bash
ssh d "mkdir deploy"
rsync -r /home/dadou/Nextcloud/Didier/python/dadou_robot/* d:./deploy/