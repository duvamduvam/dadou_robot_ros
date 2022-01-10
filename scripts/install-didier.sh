#!/bin/bash

if [ ! -d "deploy" ];then
  mkdir deploy
fi
apt install python3
pip3 install adafruit-blinka adafruit-circuitpython-neopixel adafruit-circuitpython-led-animation board jsonpath_rw jsonpath_rw_ext libatlas-base-dev pyaudio sound-player
