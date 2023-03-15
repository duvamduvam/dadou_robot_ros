#!/bin/bash

# activate i2c
printf "${RED}activate i2c${CYAN}\n"
raspi-config nonint do_i2c 0