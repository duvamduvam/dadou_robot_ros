#!/usr/bin/env python3
import logging

import rclpy
from adafruit_led_animation.helper import PixelSubset
from rclpy.node import Node
import time
import neopixel

from DadouRobot.dadourobot.files.robot_json_manager import RobotJsonManager
from dadou_utils.utils_static import LIGHTS_START_LED, LIGHTS_END_LED, ROBOT_LIGHTS, JSON_LIGHTS, LIGHTS_LED_COUNT, \
    BRIGHTNESS, LIGHTS_PIN
from dadourobot.actions.face import Face
from dadourobot.actions.lights import Lights
from dadourobot.actions.wheel import Wheel
from dadourobot.robot_config import config


class LightsNode(Node):
    def __init__(self):
        super().__init__("node_name")
        robot_json_manager = RobotJsonManager(config)
        pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False,
                                   brightness=config[BRIGHTNESS])

        face_strip = PixelSubset(pixels, 0, config[LIGHTS_START_LED] - 1)
        self.face = Face(config, robot_json_manager, face_strip)

        self.subscriber_ = self.create_subscription(RobotMsg, "robot_msg", self.robot_news_callback, 10)
        self.get_logger().info("smartphone have been started")

    def robot_news_callback(self, msg):
        self.get_logger().info(msg.data)
        self.face.update(msg.data)

    def run(self):
        while True:
            try:
                self.face.process()
                time.sleep(0.001)
            except Exception as err:
                logging.error('exception {}'.format(err), exc_info=True)

def main(args=None):
    rclpy.init(args=args)
    node = LightsNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
