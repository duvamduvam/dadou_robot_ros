import logging.config
import os
import time

import neopixel

from dadou_utils_ros.logging_conf import LoggingConf
from dadou_utils_ros.utils.time_utils import TimeUtils
from dadou_utils_ros.utils_static import LIGHTS_LED_COUNT, BRIGHTNESS, LIGHTS_PIN, UNITTEST, LOGGING_TEST_FILE_NAME, \
    FACE
from robot.actions.face import Face
from robot.files.robot_json_manager import RobotJsonManager
from robot.robot_config import config
from robot.tests.conf_test import TestSetup
from robot.visual.image_mapping import ImageMapping
from robot.visual.visual import Visual

#TestSetup()


import unittest


class TestFace(unittest.TestCase):

    logging.config.dictConfig(LoggingConf.get(config[LOGGING_TEST_FILE_NAME], "test_face"))

    robot_json_manager = RobotJsonManager(config)
    pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False,
                                   brightness=config[BRIGHTNESS])

    face = Face(config=config, json_manager=robot_json_manager, strip=pixels)

    logging.info("start face test")

    def test_default(self):
        while True:
            self.face.process()
            time.sleep(0.01)

    def test_fuzz(self):
        self.face.update({FACE: "fuzz"})
        while True:
            self.face.process()
            time.sleep(0.01)

    @unittest.skip
    def test_something(self):
        self.face.pixels.fill(BLACK)
        visual = Visual.get_visual("test", self.face.visuals)
        self.image_mapping.mapping(self.face.pixels, visual.rgb)
        self.face.pixels.show()
        # time.sleep(10)

    @unittest.skip
    def test_img_mouth(self):
        logging.info("test_img_mouth")
        self.face.pixels.fill(BLACK)
        visual = Visual.get_visual("mopen1", self.face.visuals)
        # self.face.fill_matrix(0, self.face.mouth_end, visual)
        self.face.pixels[(8 * 8 * 2)] = AMBER
        self.face.pixels[(8 * 8 * 2) + 1] = AMBER
        self.face.pixels[(8 * 8 * 2) + 2] = AMBER
        self.face.pixels[(8 * 8 * 2) + 3] = AMBER
        self.face.pixels[(8 * 8 * 2) + 4] = AMBER
        self.face.pixels[(8 * 8 * 2) + 5] = AMBER
        self.face.pixels[(8 * 8 * 2) + 6] = AMBER
        self.face.pixels[(8 * 8 * 2) + 7] = AMBER
        self.face.pixels[220] = RED

        self.face.pixels.show()
        time.sleep(10)

    def test_face2(self):
        logging.info("animate face A1")
        self.face.update("default")
        start_time =TimeUtils.current_milli_time()
        while not TimeUtils.is_time(start_time, 10000):
            # logging.info("animate")
            self.face.animate()

    def test_basic(self):
        pixels = neopixel.NeoPixel(board.D21, 8 * 6 * 8, auto_write=False)
        pixels.brightness = 0.1
        while True:
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels[5] = (255, 0, 0)
            pixels[6] = (0, 255, 0)
            pixels[7] = (0, 0, 255)
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((255, 0, 0, 0))
            pixels.show()
            time.sleep(1)
