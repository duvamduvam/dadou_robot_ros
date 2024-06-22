#!/usr/bin/env python3
import json
import logging
import logging.config
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from dadou_utils_ros.logging_conf import LoggingConf
from dadou_utils_ros.utils_static import RELAYS, AUDIO, FACE, ROBOT_LIGHTS, NECK, LEFT_EYE, RIGHT_EYE, LEFT_ARM, \
    RIGHT_ARM, \
    ANIMATION, LOGGING_FILE_NAME, DURATION, STOP
from robot.files.robot_json_manager import RobotJsonManager
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config
from robot.sequences.animation_manager import AnimationManager
from robot_interfaces.msg._string_time import StringTime


PUBLISHER_LIST = [AUDIO, FACE, ROBOT_LIGHTS, RELAYS, NECK, LEFT_EYE, RIGHT_EYE, LEFT_ARM, RIGHT_ARM]


class AnimationsNode(Node):
    def __init__(self):

        node_name = ANIMATION+"_node"
        super().__init__(node_name)
        logging.config.dictConfig(LoggingConf.get(config[LOGGING_FILE_NAME], node_name))

        robot_json_manager = RobotJsonManager(config)
        self.animations_manager = AnimationManager(config, robot_json_manager)

        self.action_publishers = {}
        for p in PUBLISHER_LIST:
            self.action_publishers[p] = self.create_publisher(StringTime, p, 10)

        logging.info("Starting {}".format(node_name))

        self.subscription = self.create_subscription(
            StringTime,
            ANIMATION,
            self.listener_callback,
            10)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def listener_callback(self, ros_msg):
        logging.info("input : {}".format(ros_msg))
        animation_msg = {ANIMATION: json.loads(ros_msg.msg)}
        if ros_msg.time != 0:
            animation_msg[DURATION] = ros_msg.time
        animations_msg = self.animations_manager.update(animation_msg)
        self.send_msgs(animations_msg)

    def timer_callback(self):
        # Logique à exécuter en continu ici
        try:
            animations_msg = self.animations_manager.process()
            if animations_msg:
                self.send_msgs(animations_msg)
        except Exception as e:
            logging.error(e, exc_info=True)

    def send_msgs(self, animations_msg):
        logging.info("animations msg to publish {}".format(animations_msg))

        if ANIMATION in animations_msg and not animations_msg[ANIMATION]:
            logging.info("send animations stop")
            msg = StringTime()
            msg.msg = json.dumps(STOP)
            for p in self.action_publishers:
                self.action_publishers[p].publish(msg)
            return

        if isinstance(animations_msg, dict):
            for k, v in animations_msg.items():
                if k in self.action_publishers:
                    logging.info("publish {} in {}".format(v, k))

                    msg = StringTime()
                    msg.msg = json.dumps(v)
                    if DURATION in animations_msg and animations_msg[DURATION] != 0:
                        msg.time = animations_msg[DURATION]
                    self.action_publishers[k].publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = AnimationsNode()
    try:
        while rclpy.ok():
            try:
                rclpy.spin_once(node)
            except Exception as e:
                logging.error(e, exc_info=True)
    except Exception as e:
        logging.error(e, exc_info=True)
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
