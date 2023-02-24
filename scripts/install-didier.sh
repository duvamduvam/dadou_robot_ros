#!/bin/bash

home=/home/didier
deploy=$home/deploy

if [ ! -d "deploy" ];then
  mkdir deploy
fi

# install librairies
sudo apt update
sudo apt upgrade

# install .bashrc
ln -sf $deploy/scripts/bashrc ~/.bashrc
ln -sf $deploy/scripts/bashrc /root/.bashrc
source $home/.bashrc

# ssh root
sudo mkdir /root/.ssh/
#TODO fix cp: impossible d'évaluer '/home/didier/.ssh/authorized_keys': Aucun fichier ou dossier de ce type
sudo cp $home/.ssh/authorized_keys /root/.ssh/

# pip alias
sudo ln -sf /usr/local/bin/pip3 /usr/bin/pip3.9
sudo ln -sf /usr/local/bin/pip3 /usr/bin/pip3
sudo ln -sf /usr/local/bin/pip3 /usr/bin/pip

sudo pip3 install --upgrade pip
#install pycharm helper
pip3 install --no-index /home/didier/.pycharm_helpers/setuptools-44.1.1-py2.py3-none-any.whl

source install-lib.sh

# install service
sudo ln -sf $deploy/scripts/didier.service /etc/systemd/system/
sudo chmod 644 $deploy/scripts/didier.service
sudo chown root:root $deploy/scripts/didier.service
sudo systemctl enable didier.service
sudo systemctl daemon-reload

# install alsa
sudo ln -sf $deploy/scripts/.asoundrc $home
sudo ln -sf $deploy/scripts/.asoundrc /root

# .bashrc
sudo ln -sf $deploy/scripts/.bashrc $home
sudo ln -sf $deploy/scripts/.bashrc /root

echo set mouse-=a > ~/.vimrc
sudo echo set mouse-=a > ~/.vimrc
