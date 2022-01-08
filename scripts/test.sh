#!/bin/bash

cd /home/pi/deploy/didier-python/
sudo python3 -m unittest python/tests/$1 $2
