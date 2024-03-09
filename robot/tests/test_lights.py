import logging
import os

from dadou_utils.utils.time_utils import TimeUtils
from robot.actions import Lights
from robot.files.robot_json_manager import RobotJsonManager
from robot.robot_config import JSON_DIRECTORY, JSON_CONFIG
from robot.tests.conf_test import TestSetup

TestSetup()

import time
import unittest

import board
import neopixel
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.helper import PixelMap
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation import color


class LightsTest(unittest.TestCase):
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    BLACK = (0, 0, 0)

    base_path = os.getcwd()
    robot_json_manager = RobotJsonManager(base_path, "/.."+JSON_DIRECTORY, JSON_CONFIG)
    config = RobotConfig(robot_json_manager)

    pixel_pin = board.D18

    # The number of NeoPixels
    num_pixels = 30

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    lights = Lights(config, robot_json_manager, pixels)

    def test_lights_key(self):
        current_time = TimeUtils.current_milli_time()
        while not TimeUtils.is_time(current_time, 2000):
            self.lights.animate()

        keys = {"C2", "C3", "C10"}
        for k in keys:
            logging.info("test lights key " + k)
            self.lights.update(k)
            current_time = TimeUtils.current_milli_time()
            while not TimeUtils.is_time(current_time, 10000):
                self.lights.animate()

    def test_lights_default(self):
        # self.lights.update("B1")
        while True:
            self.lights.animate()

    @unittest.skip
    def test_color_chase(self):
        pixels = neopixel.NeoPixel(board.D18, 8 * 6 * 8, auto_write=False)
        pixels.brightness = 0.1
        # pixel_wing_vertical = helper.PixelMap.vertical_lines(
        #    pixels, 8, 8, helper.horizontal_strip_gridmap(8, alternating=False)
        # )

        # comet_v = Comet(pixel_wing_vertical, speed=0.1, color=AMBER, tail_length=6, bounce=True)

        m1 = PixelMap(pixels, [(0, 64)])
        m2 = PixelMap(pixels, [(64, 128)])
        m3 = PixelMap(pixels, [(129, 192)])
        m4 = PixelMap(pixels, [(193, 256)])
        m5 = PixelMap(pixels, [(257, 320)])
        m6 = PixelMap(pixels, [(321, 384)])

        mf = PixelMap(pixels, [(0, 384)])

        m1[0] = (255, 255, 0)
        m2[0] = (255, 255, 0)
        m3[0] = (255, 255, 0)
        m4[0] = (255, 0, 255)
        m5[0] = (255, 0, 255)
        m6[0] = (255, 0, 255)

        animations = AnimationSequence(
            # Synchronized to 0.5 seconds. Ignores the second animation setting of 3 seconds.
            AnimationGroup(
                RainbowComet(mf, speed=0.1, tail_length=7, bounce=True),
                Blink(m2, 3.0, color.AMBER),
                sync=True,
            ),
            # Different speeds
            AnimationGroup(
                Comet(m3, 0.1, color.MAGENTA, tail_length=5),
                Comet(m4, 0.01, color.MAGENTA, tail_length=15),
            ),
            # Different animations
            AnimationGroup(
                Blink(m5, 0.5, color.JADE),
                Comet(m6, 0.05, color.TEAL, tail_length=15),
            ),
            # Sequential animations on the built-in NeoPixels then the NeoPixel strip
            # Chase(m1, 0.05, size=2, spacing=3, color=color.PURPLE),
            # Chase(m2, 0.05, size=2, spacing=3, color=color.PURPLE),
            advance_interval=3.0,
            auto_clear=True,
            auto_reset=True,
        )

        while True:
            animations.animate()

    @unittest.skip
    def test_rainbow_cycle(self):
        self.lights.clean()
        self.lights.rainbow_cycle(0.1)

    @unittest.skip
    def test_random(self):
        for i in range(10000):
            self.lights.random()
            time.sleep(0.05)
            self.lights.clean()

    @unittest.skip
    def test_full_color(self):
        self.lights.fill(self.BLUE)
        time.sleep(2)
        self.lights.fill(self.YELLOW)
        time.sleep(2)
        self.lights.fill(self.CYAN)
        time.sleep(2)
        self.lights.fill(self.RED)
        time.sleep(2)
        self.lights.fill(self.PURPLE)
        time.sleep(2)
        self.lights.fill(self.BLACK)
        time.sleep(2)
