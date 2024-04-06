#!/usr/bin/env python3
import logging

import rclpy
from adafruit_led_animation.helper import PixelSubset
from rclpy.node import Node
import time
import neopixel

from dadou_utils_ros.utils_static import LIGHTS_START_LED, LIGHTS_LED_COUNT, \
    BRIGHTNESS, LIGHTS_PIN, ROBOT_LIGHTS, FACE, AUDIO
from robot.actions.audio_manager import AudioManager
from robot.files.robot_json_manager import RobotJsonManager
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class AudioNode(SubscriberNode):
    def __init__(self):
        robot_json_manager = RobotJsonManager(config)
        self.audio = AudioManager(config, robot_json_manager)

        super().__init__(AUDIO , AUDIO, self.audio)

def main(args=None):
    rclpy.init(args=args)
    node = AudioNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
