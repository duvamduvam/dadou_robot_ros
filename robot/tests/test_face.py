import logging.config

from hardrive.files import RobotJsonManager

from robot.robot_config import RobotConfig
from robot.tests.conf_test import TestSetup
from robot.utils import Utils
from robot.visual.image_mapping import ImageMapping
from robot.visual.visual import Visual

TestSetup()

import time
import neopixel
import board

from adafruit_led_animation.color import RED, BLACK, AMBER

import unittest


class TestFace(unittest.TestCase):
    json_manager = RobotJsonManager(RobotConfig.BASE_PATH)
    face = Face(json_manager)
    logging.info("start face test")
    image_mapping = ImageMapping(8, 8, 3, 2)

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
        start_time = Utils.current_milli_time()
        while not Utils.is_time(start_time, 10000):
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

    """def test_img_eye(self):
        path = self.json_manager.get_visual_path("eye-still")
        visual = Visual("eye-still", path)
        # self.face.pixels[10] = visual.rgb[2][2]
        self.face.pixels.fill((0, 0, 0))
        self.face.pixels.show()
        self.face.fill_matrix(0, 64, visual)
        self.face.pixels.show()
        time.sleep(1)"""
