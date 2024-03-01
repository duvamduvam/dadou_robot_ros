#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node

from dadourobot.actions.wheel import Wheel
from dadourobot.robot_config import config


class WheelsNode(Node):
    def __init__(self):
        super().__init__("node_name")
        self.wheels = Wheel(config)
        self.subscriber_ = self.create_subscription(RobotMsg, "robot_msg", self.robot_news_callback, 10)
        self.get_logger().info("smartphone have been started")

    def robot_news_callback(self, msg):
        self.get_logger().info(msg.data)
        self.wheels.update(msg.data)

    def run(self):
        while True:
            try:
                self.wheels.process()
                time.sleep(0.001)
            except Exception as err:
                logging.error('exception {}'.format(err), exc_info=True)

def main(args=None):
    rclpy.init(args=args)
    node = WheelsNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
