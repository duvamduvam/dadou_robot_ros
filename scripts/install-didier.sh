#!/bin/bash

home=/home/didier
deploy=$home/deploy
scripts=$deploy/scripts/
rpi_conf=$deploy/conf/rpi

RED='\033[4;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

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
source $scripts/install-lib.sh

# install sound config usb
printf "${RED}configure sound${CYAN}\n"
cp $rpi_conf/alsa-blacklist.conf /etc/modprobe.d
ln -sf $rpi_conf/asoundrc $home/.asoundrc
ln -sf $rpi_conf/asoundrc /root/.asoundrc

# activate i2c
printf "${RED}activate i2c${CYAN}\n"
raspi-config nonint do_i2c 0

# install bashrc
printf "${RED}install bash configuration${CYAN}\n"
ln -sf $rpi_conf/bashrc $home/.bashrc
ln -sf $rpi_conf/bashrc /root/.bashrc

#install vim config
printf "${RED}update vim parameter${CYAN}\n"
echo set mouse-=a > ~/.vimrc
echo set mouse-=a > ~/.vimrc

# install service
printf "${RED}install service${CYAN}\n"
ln -sf $rpi_conf/didier.service /etc/systemd/system/
chmod 644 $rpi_conf/didier.service
chown root:root $rpi_conf/didier.service
systemctl enable didier.service
systemctl daemon-reload
service didier start