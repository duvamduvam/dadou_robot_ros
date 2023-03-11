#!/bin/bash

if [ -z "$1" ]
then
      host="dr"
else
      host=$1
fi

rsync -auvzr /home/dadou/Nextcloud/Didier/python/dadou_robot/audios/* $host:/home/didier/deploy/audios/