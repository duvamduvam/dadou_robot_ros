#!/usr/bin/env python3
import logging

import rclpy
from adafruit_led_animation.helper import PixelSubset
from rclpy.node import Node
import time
import neopixel

from robot.files.robot_json_manager import RobotJsonManager
from dadou_utils.utils_static import LIGHTS_START_LED, LIGHTS_LED_COUNT, \
    BRIGHTNESS, LIGHTS_PIN, ROBOT_LIGHTS, FACE
from robot.actions.face import Face
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class FaceNode(SubscriberNode):
    def __init__(self):
        robot_json_manager = RobotJsonManager(config)
        pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False,
                                   brightness=config[BRIGHTNESS])

        face_strip = PixelSubset(pixels, 0, config[LIGHTS_START_LED] - 1)
        self.face = Face(config=config, json_manager=robot_json_manager, strip=face_strip)

        super().__init__(FACE, FACE, self.face)

def main(args=None):
    rclpy.init(args=args)
    node = FaceNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
