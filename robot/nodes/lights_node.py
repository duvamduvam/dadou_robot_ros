#!/usr/bin/env python3
import logging
import logging.config

import rclpy
from std_msgs.msg import String
from adafruit_led_animation.helper import PixelSubset
from rclpy.node import Node
import time
import neopixel

from robot.files.robot_json_manager import RobotJsonManager
from dadou_utils_ros.utils_static import LIGHTS_START_LED, LIGHTS_LED_COUNT, \
    BRIGHTNESS, LIGHTS_PIN, ROBOT_LIGHTS, FACE, LIGHTS_END_LED, JSON_LIGHTS, LIGHTS, LOGGING_FILE_NAME
from robot.actions.face import Face
from robot.actions.lights import Lights
from robot.robot_config import config
from dadou_utils_ros.logging_conf import LoggingConf


class LightsNode(Node):
    def __init__(self):
        node_name = 'lights_node'
        super().__init__(node_name)

        logging.info("starting {}".format(node_name))

        robot_json_manager = RobotJsonManager(config)
        pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False,
                                   brightness=config[BRIGHTNESS])

        self.face = Face(config=config, json_manager=robot_json_manager, strip=pixels)
        self.lights = Lights(config=config, start=config[LIGHTS_START_LED], end=config[LIGHTS_END_LED],
            json_manager=robot_json_manager, global_strip=pixels, light_type=ROBOT_LIGHTS, json_light=config[JSON_LIGHTS])

        self.lights_subscription = self.create_subscription(
            String, ROBOT_LIGHTS, self.lights_callback, 10)

        self.face_subscription = self.create_subscription(
            String, FACE, self.face_callback, 10)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def face_callback(self, ros_msg):
        msg = ros_msg.data
        logging.info('Face: "%s"' % msg)
        self.face.update({FACE: msg})

    def lights_callback(self, ros_msg):
        msg = ros_msg.data
        logging.info('Lights: "%s"' % msg)
        self.lights.update({ROBOT_LIGHTS: msg})

    def timer_callback(self):
        self.face.process()
        self.lights.process()

def main(args=None):
    rclpy.init(args=args)
    node = LightsNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
