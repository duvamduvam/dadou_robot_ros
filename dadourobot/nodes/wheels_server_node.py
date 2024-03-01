#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class WheelsServerNode(Node):
    def __init__(self):
        super().__init__("wheels_server")
        self.counter = 0
        self.get_logger().info("Hello ROS2")
        self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        self.counter += 1
        self.get_logger().info("Hello Timer {}".format(self.counter))


def main(args=None):
    rclpy.init(args=args)
    node = WheelsServerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()