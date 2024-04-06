#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node

from dadou_utils_ros.utils.status import Status
from dadou_utils_ros.utils_static import RELAYS, SHUTDOWN_PIN, STATUS_LED_PIN, RESTART_PIN, SYSTEM
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class SystemNode(SubscriberNode):
    def __init__(self):
        self.system = Status(config[SHUTDOWN_PIN], config[STATUS_LED_PIN], config[RESTART_PIN])

        super().__init__(SYSTEM, SYSTEM, self.system)


def main(args=None):
    rclpy.init(args=args)
    node = SystemNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

















