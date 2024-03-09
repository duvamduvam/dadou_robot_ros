#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node

from dadou_utils.utils_static import RELAYS
from robot.actions.relays import RelaysManager
from robot.files.robot_json_manager import RobotJsonManager
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class RelaysNode(SubscriberNode):
    def __init__(self):
        robot_json_manager = RobotJsonManager(config)
        self.relays = RelaysManager(config, robot_json_manager)
        super().__init__(RELAYS, RELAYS, self.relays)


def main(args=None):
    rclpy.init(args=args)
    node = RelaysNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()