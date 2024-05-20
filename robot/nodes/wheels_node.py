#!/usr/bin/env python3
import json
import logging

import rclpy

from dadou_utils_ros.utils_static import WHEELS, WHEEL_LEFT, WHEEL_RIGHT, DURATION
from robot.actions.wheels import Wheels
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class WheelsNode(SubscriberNode):
    def __init__(self):

        self.wheels = Wheels(config)
        super().__init__(WHEELS, WHEELS, self.wheels)

def main(args=None):
    try:
        rclpy.init(args=args)
        node = WheelsNode()
        rclpy.spin(node)
        rclpy.shutdown()
    except Exception as e:
        logging.error(e, exc_info=True)

if __name__ == '__main__':
    main()
