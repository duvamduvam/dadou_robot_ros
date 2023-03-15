#!/bin/bash

source params-robot.sh

if [ "$1" ]; then
  python_file=$1
else
  python_file='main.py'
fi

#aplay /home/didier/deploy/audios/start.mp3
cd /home/didier/deploy/dadourobot
  export PYTHONPATH="$DEPLOY, $DEPLOY/$PROJECT_NAME, $UTILS_PROJECTS, /usr/lib/python39.zip, /usr/lib/python3.9, /usr/lib/python3.9/lib-dynload, /usr/local/lib/python3.9/dist-packages, /usr/lib/python3/dist-packages, /usr/lib/python3.9/dist-packages, ."
echo $PYTHONPATH
python3 $python_file
