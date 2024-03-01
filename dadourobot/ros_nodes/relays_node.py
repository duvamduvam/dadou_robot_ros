#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node

from dadourobot.actions.relays import RelaysManager
from dadourobot.actions.wheel import Wheel
from dadourobot.files.robot_json_manager import RobotJsonManager
from dadourobot.robot_config import config


class RelaysNode(Node):
    def __init__(self):
        super().__init__("node_name")
        robot_json_manager = RobotJsonManager(config)
        self.relays = RelaysManager(config, robot_json_manager)
        self.subscriber_ = self.create_subscription(RobotMsg, "robot_msg", self.robot_news_callback, 10)
        self.get_logger().info("relays have been started")

    def robot_news_callback(self, msg):
        self.get_logger().info(msg.data)
        self.relays.update(msg.data)

    def run(self):
        while True:
            try:
                self.relays.process()
                time.sleep(0.001)
            except Exception as err:
                logging.error('exception {}'.format(err), exc_info=True)

def main(args=None):
    rclpy.init(args=args)
    node = RelaysNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
