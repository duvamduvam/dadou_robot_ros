import logging.config
from python.tests.conf_test import TestSetup
TestSetup()

import time
import neopixel
import board
from python.json_manager import JsonManager
from python.visual import Visual
from python.actions.face import Face
from python.tests.conf_test import TestSetup

import unittest


class MyTestCase(unittest.TestCase):
    json_manager = JsonManager()
    face = Face()

    def test_img_eye(self):
        print("animate face A1")
        self.face.update("A1")
        while True:
            print("animate")
            self.face.animate()

    @unittest.skip
    def test_basic(self):
        pixels = neopixel.NeoPixel(board.D18, 8 * 6 * 8, auto_write=False)
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

    @unittest.skip
    def test_img_eye(self):
        path = self.json_manager.get_visual_path("eye-still")
        visual = Visual("eye-still", path)
        #self.face.pixels[10] = visual.rgb[2][2]
        self.face.pixels.fill((0, 0, 0))
        self.face.pixels.show()
        self.face.fill_matrix(0, 64, visual)
        self.face.pixels.show()
        time.sleep(1)

