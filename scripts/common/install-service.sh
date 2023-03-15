#!/bin/bash

if [ -z "$1" ]
then
      printf "${RED}! no service name !${NF}\n"
else
      service_name=$1
fi

if [ -z "$RPI_CONF" ]
then
      echo "\$RPI_CONF is empty"
      exit 0
fi

# install service
printf "${RED}install service${CYAN}\n"
ln -sf $RPI_CONF/$service_name.service /etc/systemd/system/
chmod 644 $RPI_CONF/$service_name.service
chown root:root $RPI_CONF/$service_name.service
systemctl enable $service_name.service
systemctl daemon-reload
service $service_name start