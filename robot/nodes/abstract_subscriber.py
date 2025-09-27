#!/usr/bin/env python3
import json
import logging
import logging.config

import rclpy
from rclpy.node import Node

from dadou_utils_ros.logging_conf import LoggingConf
from dadou_utils_ros.utils_static import LOGGING_FILE_NAME, DURATION, ANIMATION
from robot_interfaces.msg._string_time import StringTime

class SubscriberNode(Node):
    def __init__(self, config, action_type, topic_name, action):
        self.action_type = action_type
        node_name = action_type + "_node"
        print(config[LOGGING_FILE_NAME])
        logging.config.dictConfig(LoggingConf.get(config[LOGGING_FILE_NAME], node_name))

        super().__init__(node_name)

        self.action = action

        logging.info("Starting {} with topic {}".format(node_name, topic_name))

        self.subscription = self.create_subscription(
            StringTime,
            topic_name,
            self.listener_callback,
            10)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def listener_callback(self, ros_msg):
        msg = json.loads(ros_msg.msg)
        logging.info("input {} : ".format(ros_msg))
        action_msg = {self.action_type: msg}
        action_msg[ANIMATION] = ros_msg.anim
        if ros_msg.time != 0:
            action_msg[DURATION] = ros_msg.time
        self.action.update(action_msg)
    def timer_callback(self):
        # Logique à exécuter en continu ici
        logging.debug('Action en temps réel')
        try:
            self.action.process()
        except Exception as e:
            logging.error(e, exc_info=True)
