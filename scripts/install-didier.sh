#!/bin/bash

if [ ! -d "deploy" ];then
  mkdir deploy
fi
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-dev python3-pip python3-opencv python3-rpi.gpio libatlas-base-dev libopenjp2-7 vim
./install-lib.sh
#fix sound reinstall pulseaudio
#fix : OSError: [Errno 25] Inappropriate ioctl for device
#sudo nano /boot/config.txt
 #Add below line to the end of the file
 #
 #dtoverlay=pi3-miniuart-bt
 #Save and exit from nano and reboot your Raspberry.
 #
 #
 #
 #If you’re still getting error;
 #
 #sudo raspi-config
 #Hit Interface Options > Serial Port

#Login shell over serial?: No
#Serial port hardware enabled?: Yes
#reboot
