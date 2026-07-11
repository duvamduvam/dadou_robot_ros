#!/usr/bin/env python3
import logging

import rclpy
from rclpy.node import Node
import time

from robot.robot_static import LIGHTS_START_LED, LIGHTS_LED_COUNT, LIGHTS_PIN
from dadou_utils_ros.utils_static import BRIGHTNESS, ROBOT_LIGHTS, FACE, AUDIO
from robot.actions.audio_manager import AudioManager
from robot.files.robot_json_manager import RobotJsonManager
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class AudioNode(SubscriberNode):
    def __init__(self):
        robot_json_manager = RobotJsonManager(config)
        self.audio = AudioManager(config, robot_json_manager)

        super().__init__(config, AUDIO, AUDIO, self.audio)

def main(args=None):
    rclpy.init(args=args)
    node = AudioNode()
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
