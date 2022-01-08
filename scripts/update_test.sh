#!/bin/bash

/home/pi/scripts/push_from_home.sh > /dev/console
/home/pi/scripts/test.sh $1 $2 > /dev/console
