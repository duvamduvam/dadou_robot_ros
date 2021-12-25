import time
import unittest

import board
import neopixel
from adafruit_led_animation import helper
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import AMBER
from adafruit_led_animation.helper import PixelMap

from python.actions.lights import Lights


class LightsTest(unittest.TestCase):
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    BLACK = (0, 0, 0)

    lights = Lights()


    def test_color_chase(self):
        pixels = neopixel.NeoPixel(board.D18, 8*6*8, auto_write=False)
        pixels.brightness = 0.1
        pixel_wing_vertical = helper.PixelMap.vertical_lines(
            pixels, 8*6, 8, helper.horizontal_strip_gridmap(8, alternating=False)
        )

        comet_v = Comet(pixel_wing_vertical, speed=0.1, color=AMBER, tail_length=6, bounce=True)

        while True:
            comet_v.animate()

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
