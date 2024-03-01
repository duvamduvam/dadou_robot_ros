#!/bin/bash
set -x

####################### PROJECT PARAMS #############################

export PROJECT_NAME="dadourobot"
export PROJECT_PATH=~/Nextcloud/Didier/python/dadou_robot_ros
export UTILS_PROJECT=~/Nextcloud/Didier/python/dadou_utils_ros

#export USER_HOST="r"
#export ROOT_HOST="rr"
#export RPI_IP="192.168.1.200"
#export RPI_HOST_NAME="didier.local"

export USER_HOST="ros-robot"
export ROOT_HOST="ros-robot-root"
#export RPI_IP="192.168.1.200"
export RPI_HOST_NAME="ros-robot.local"

#export INSTALL_LIB="yes"
export SET_USB_AUDIO="yes"
export ACTIVATE_I2C="yes"
export SET_BASHRC="yes"
export SET_VIMRC="yes"
export INSTALL_SERVICE="yes"
#export INSTALL_AUTOSTART="yes"
export INSTALL_DOCKER="yes"

export SERVICE_NAME=didier


export PROJECT_SYSTEM_LIB="python3-opencv portaudio19-dev python3-pyaudio mpg123 libcairo2-dev libgirepository1.0-dev"
export PROJECT_PYTHON_LIB="imageio adafruit-circuitpython-servokit adafruit-circuitpython-rfm9x watchdog adafruit-circuitpython-bno055 adafruit-circuitpython-neopixel simpleaudio playsound openai whisper"

export LOG_FILE="robot.log"

####################################################################

#export RPI_HOME=/home/didier
export RPI_HOME=/home/robot
export LOCAL_HOME=~

export UTILS_PROJECT=$LOCAL_HOME/Nextcloud/Didier/python/dadou_utils
export UTILS_SCRIPTS=$UTILS_PROJECT/scripts/deploy

declare -A PROJECT_DEPENDENCIES
PROJECT_DEPENDENCIES[0]=$UTILS_PROJECT
export PROJECT_DEPENDENCIES
#printf "$PROJECT_DEPENDENCIES[@]"

if [ "$1" = "read_param" ]; then
  printf "${CYAN}Only read param${CYAN}\n"
  if [ -d "$RPI_SCRIPTS" ]; then
    printf "$RPI_SCRIPTS/params.sh\n"
  fi
  if [ -d "$UTILS_SCRIPTS" ]; then
    printf "$UTILS_SCRIPTS/params.sh\n"
  fi
else
  printf "${CYAN}$UTILS_SCRIPTS/deploy-utils.sh $1${CYAN}\n"
  source $UTILS_SCRIPTS/deploy-utils.sh $1
fi

#set +x

#!/bin/bash

export RPI_DEPLOY=$RPI_HOME/deploy/src
export RPI_CONF=$RPI_DEPLOY/conf/rpi
export RPI_SCRIPTS=$RPI_DEPLOY/scripts
export RPI_LOGS=$RPI_DEPLOY/logs/
export RPI_PYTHON_LIB=/usr/lib/python3/dist-packages
export UTILS_RPI_CONF=$UTILS_PROJECT/conf/rpi

export SYSTEM_LIB="ffmpeg i2c-tools python3 python3-dev python3-pip libatlas-base-dev libopenjp2-7 libasound2-dev vim"
export PYTHON_LIB="Adafruit-Blinka adafruit-io adafruit-circuitpython-neopixel adafruit-circuitpython-led-animation adafruit-circuitpython-pcf8574 adafruit-circuitpython-servokit colorlog filetype pydub imageio inotify jsonpath_rw jsonpath_rw_ext psutil pyserial rpi_ws281x sound-player uvloop watchdog websocket-client websockets"
#adafruit-circuitpython-motor schedule

declare -A LIB_SYMLINK
LIB_SYMLINK[0]=/usr/lib/python3.9/dist-packages
LIB_SYMLINK[1]=/usr/local/lib/python3/dist-packages
LIB_SYMLINK[2]=/usr/local/lib/python3.9/dist-packages
export LIB_SYMLINK
#printf "$LIB_SYMLINK[@]"