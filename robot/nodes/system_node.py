#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node

from dadou_utils_ros.utils.status import Status
from dadou_utils_ros.utils_static import RELAYS, SHUTDOWN_PIN, STATUS_LED_PIN, RESTART_PIN, SYSTEM, I2C_ENABLED, \
    DIGITAL_CHANNELS_ENABLED
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class SystemNode(SubscriberNode):
    def __init__(self):
        self.system = Status(config)

        super().__init__(SYSTEM, SYSTEM, self.system)


def main(args=None):
    try:
        rclpy.init(args=args)
        node = SystemNode()
        rclpy.spin(node)
        rclpy.shutdown()
    except Exception as e:
        logging.error(e, exc_info=True)


if __name__ == '__main__':
    main()

















