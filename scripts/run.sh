#!/bin/bash

if [ "$1" ]; then
  python_file=$1
else
  python_file='main.py'
fi

#aplay /home/didier/deploy/audios/start.mp3
cd /home/didier/deploy/dadourobot
  export PYTHONPATH="/home/didier/deploy/, /home/didier/deploy/dadourobot, /home/dadou/Nextcloud/Didier/python/dadou_control, /home/didier/deploy, /home/dadou/Nextcloud/Didier/python/dadou_utils, /home/didier/.pycharm_helpers/pycharm_display, /usr/lib/python39.zip, /usr/lib/python3.9, /usr/lib/python3.9/lib-dynload, /home/didier/.local/lib/python3.9/site-packages, /usr/local/lib/python3.9/dist-packages, /usr/lib/python3/dist-packages, /usr/lib/python3.9/dist-packages, /home/didier/.pycharm_helpers/pycharm_matplotlib_backend, /home/didier/deploy/dadourobot, ."
echo $PYTHONPATH
python3 $python_file
