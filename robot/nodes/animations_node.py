#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from dadou_utils.utils_static import RELAYS, AUDIO, FACE, ROBOT_LIGHTS, NECK, LEFT_EYE, RIGHT_EYE, LEFT_ARM, RIGHT_ARM, \
    ANIMATIONS
from robot.files.robot_json_manager import RobotJsonManager
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config
from robot.sequences.animation_manager import AnimationManager


PUBLISHER_LIST = [AUDIO, FACE, ROBOT_LIGHTS, RELAYS, NECK,LEFT_EYE, RIGHT_EYE, LEFT_ARM, RIGHT_ARM]


class AnimationsNode(SubscriberNode):
    def __init__(self):
        robot_json_manager = RobotJsonManager(config)
        self.animations_manager = AnimationManager(config, robot_json_manager)

        super().__init__(ANIMATIONS, RELAYS, self.animations_manager)

        self.action_publishers = {}
        for p in PUBLISHER_LIST:
            self.action_publishers[p] = self.create_publisher(String, p, 10)

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        animations_msg = self.action.update(msg)
        self.send_msgs(animations_msg)

    def timer_callback(self):
        # Logique à exécuter en continu ici
        self.get_logger().debug('Action en temps réel')
        animations_msg = self.action.process()
        self.send_msgs(animations_msg)

    def send_msgs(self, animations_msg):
        if animations_msg and isinstance(animations_msg, dict):
            for k, v in animations_msg.items():
                if k in self.action_publishers:
                    self.get_logger().info("publish {} in {}".format(v, k))
                    self.action_publishers[k].publish(v)

def main(args=None):
    rclpy.init(args=args)
    node = AnimationsNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
