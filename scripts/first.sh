#!/bin/bash

ssh -t d sudo raspi-config nonint do_i2c 0
ssh -t d sudo cp -r /home/didier/.ssh /root/

source before-lunch.sh

ssh dr 'bash -s < /home/didier/deploy/scripts/install-lib.sh'
ssh dr 'bash -s < /home/didier/deploy/scripts/install-didier.sh'