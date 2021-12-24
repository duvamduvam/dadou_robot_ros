import time
import unittest

import board
import neopixel
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
        pixels = neopixel.NeoPixel(board.D18, 32, auto_write=False)
        pixels.brightness = 0.1
        pixel_wing_horizontal = PixelMap(pixels, [
            (0, 8, 16, 24),
            (1, 9, 17, 25),
            (2, 10, 18, 26),
            (3, 11, 19, 27),
            (4, 12, 20, 28),
            (5, 13, 21, 29),
            (6, 14, 22, 30),
            (7, 15, 23, 31),
        ], individual_pixels=True)

        pixel_wing_horizontal[0] = (255, 255, 0)
        pixel_wing_horizontal.show()
        time.sleep(20)

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
