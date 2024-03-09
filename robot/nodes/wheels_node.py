#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from dadou_utils.utils_static import WHEELS
from robot.actions.wheels import Wheels
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class WheelsNode(SubscriberNode):
    def __init__(self):

        self.wheels = Wheels(config)
        super().__init__(WHEELS, WHEELS, self.wheels)


def main(args=None):
    rclpy.init(args=args)
    node = WheelsNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
