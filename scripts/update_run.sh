#!/bin/bash

echo $(/home/pi/scripts/push_from_home.sh  -release)
echo $(/home/pi/scripts/run.sh $1 -release)
