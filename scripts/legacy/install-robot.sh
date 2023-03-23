#!/bin/bash

source params-robot.sh

# install librairies
printf "${RED}update system${CYAN}\n"
apt-get update
apt-get upgrade

# pip alias
#ln -sf /usr/local/bin/pip3 /usr/bin/pip3.9
#ln -sf /usr/local/bin/pip3 /usr/bin/pip3
#ln -sf /usr/local/bin/pip3 /usr/bin/pip


#install pycharm helper
#pip3 install --no-index /home/didier/.pycharm_helpers/setuptools-44.1.1-py2.py3-none-any.whl

#install system and python lib
source $COMMON_SCRIPTS/install-lib.sh
source $COMMON_SCRIPTS/set-usb-audio.sh
source $COMMON_SCRIPTS/activate-i2c.sh
source $COMMON_SCRIPTS/set-bashrc.sh
source $COMMON_SCRIPTS/set-vimrc.sh
source $COMMON_SCRIPTS/install-service.sh $SERVICE_NAME
sleep 10
tail -f $LOG