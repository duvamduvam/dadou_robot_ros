import logging.config
import time

import neopixel
import board
from python.json_manager import JsonManager
from python.tests.conf_test import TestSetup
from python.visual import Visual

TestSetup()

from python.actions.face import Face
from python.tests.conf_test import TestSetup

import unittest


class MyTestCase(unittest.TestCase):
    json_manager = JsonManager()
    face = Face()

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


    def test_img_mouth(self):
        logging.info("test face")
        logging.info(self.face.visuals[0].rgb)
        path = self.json_manager.get_visual_path("eye-still")
        visual = Visual("eye-still", path)
        logging.info(visual.rgb)
        #self.face.pixels[10] = visual.rgb[2][2]
        self.face.pixels.fill((255, 0, 0))
        self.face.pixels.show()
        #logging.info("test 1 pixel")
        #logging.info(visual.rgb[2][2])
        # self.face.fill_matrix(0, 64, visual)
        # self.face.pixels.show()
        time.sleep(100)
        # logging.info(visual.rgb)
