#!/bin/bash

if [ -z "$1" ]
then
      host="dr"
else
      host=$1
fi

ssh -t $host sudo raspi-config nonint do_i2c 0
#ssh -t d sudo cp -r /home/didier/.ssh /root/

source deploy.sh $host

ssh -t $host chmod +x /home/didier/deploy/scripts/*.sh
ssh $host 'bash -s < /home/didier/deploy/scripts/install-lib.sh'
ssh $host 'bash -s < /home/didier/deploy/scripts/install-didier.sh'