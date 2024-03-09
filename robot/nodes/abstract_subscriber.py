#!/usr/bin/env python3
import logging
import logging.config

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from dadou_utils.logging_conf import LoggingConf
from dadou_utils.utils_static import LOGGING_FILE_NAME
from robot.robot_config import config


class SubscriberNode(Node):
    def __init__(self, action_type, topic_name, action):
        self.action_type = action_type
        node_name = action_type + "_node"
        logging.config.dictConfig(LoggingConf.get(config[LOGGING_FILE_NAME], node_name))

        super().__init__(node_name)

        self.action = action

        self.get_logger().info("Starting {}".format(node_name))

        self.subscription = self.create_subscription(
            String,
            topic_name,
            self.listener_callback,
            10)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def listener_callback(self, ros_msg):
        msg = ros_msg.data
        self.get_logger().info('I heard: "%s"' % msg)
        self.action.update({ self.action_type: msg})
    def timer_callback(self):
        # Logique à exécuter en continu ici
        self.get_logger().debug('Action en temps réel')
        self.action.process()
