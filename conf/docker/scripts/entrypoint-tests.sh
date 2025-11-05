#!/usr/bin/env bash

set -euo pipefail

# ROS setup scripts reference optional environment variables that may not be defined
# when running with `set -u`, so temporarily relax nounset while sourcing them.
set +u
source /opt/ros/humble/setup.bash
source /home/ros2_ws/src/robot/conf/scripts/setup-robot-env.sh
set -u

exec "$@"
