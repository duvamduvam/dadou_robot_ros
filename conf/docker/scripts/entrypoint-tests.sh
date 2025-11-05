#!/usr/bin/env bash

set -euo pipefail

source /opt/ros/humble/setup.bash

TEST_ENV_SCRIPT="/home/ros2_ws/src/robot/conf/scripts/setup-robot-env.sh"
if [[ -f "${TEST_ENV_SCRIPT}" ]]; then
  # ROS helper may reference undefined variables; relax nounset temporarily.
  set +u
  # shellcheck disable=SC1090
  source "${TEST_ENV_SCRIPT}"
  set -u
else
  echo "[CI] ${TEST_ENV_SCRIPT} not found, continuing without additional robot env setup."
fi

exec "$@"
