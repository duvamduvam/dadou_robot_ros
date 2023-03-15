#!/bin/bash

printf "${RED}Install system libraries${BLUE}\n"
apt-get install -y ffmpeg i2c-tools python3 python3-dev python3-pip python3-opencv libatlas-base-dev libopenjp2-7 libasound2-dev vim

printf "${RED}${BOLD}Install python libraries${NORMAL}${PURPLE}\n\n"
pip3 install --upgrade pip
pip3.9 install adafruit-blinka adafruit-circuitpython-neopixel adafruit-circuitpython-led-animation adafruit-circuitpython-pcf8574 adafruit-circuitpython-motor adafruit-circuitpython-rfm9x adafruit-circuitpython-servokit board colorlog filetype pydub imageio jsonpath_rw jsonpath_rw_ext pyserial schedule simpleaudio sound-player uvloop websockets
