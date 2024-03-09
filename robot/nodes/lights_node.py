#!/usr/bin/env python3
import logging

import rclpy
from adafruit_led_animation.helper import PixelSubset
from rclpy.node import Node
import time
import neopixel

from robot.files.robot_json_manager import RobotJsonManager
from dadou_utils.utils_static import LIGHTS_START_LED, LIGHTS_LED_COUNT, \
    BRIGHTNESS, LIGHTS_PIN, ROBOT_LIGHTS, FACE, LIGHTS_END_LED, JSON_LIGHTS, LIGHTS
from robot.actions.lights import Lights
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class LightsNode(SubscriberNode):
    def __init__(self):
        robot_json_manager = RobotJsonManager(config)
        pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False,
                                   brightness=config[BRIGHTNESS])

        self.lights = Lights(config=config, start=config[LIGHTS_START_LED], end=config[LIGHTS_END_LED],
                                 json_manager=robot_json_manager, global_strip=pixels, light_type=ROBOT_LIGHTS, json_light=config[JSON_LIGHTS])

        super().__init__(LIGHTS, LIGHTS, self.lights)


def main(args=None):
    rclpy.init(args=args)
    node = LightsNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
