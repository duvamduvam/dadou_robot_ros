#!/usr/bin/env bash

set -euo pipefail

source /opt/ros/humble/setup.bash
source /home/ros2_ws/src/robot/conf/scripts/setup-robot-env.sh

exec "$@"
