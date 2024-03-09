import logging.config
import time

import unittest

import neopixel

from dadou_utils.utils_static import LIGHTS_PIN
from robot.robot_config import config
from robot.visual.image_mapping import ImageMapping
from robot.visual.visual import Visual


class TestImageMapping(unittest.TestCase):

    logging.info("start image mapping test")
    pixels = neopixel.NeoPixel(config[LIGHTS_PIN], 32*24, auto_write=False, brightness=0.005,
                               pixel_order=neopixel.GRB)

    visuals = []

    def test_something(self):
        image_mapping = ImageMapping(0, 8, 8, 3, 2)
        strip = []
        #self.load_visual()
        #visual = Visual.get_visual("mopen1", self.visuals)
        #self.image_mapping.mapping(strip, visual.rgb)

    def test_index_32_8_4(self):
        image_mapping = ImageMapping(0, 32, 8, 1, 3)
        image_mapping.create_matrix_vertical_index()
        image_mapping.print_index()
        time.sleep(0.5)

    def test_index_32_8_4_image(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        image_mapping = ImageMapping(0, 32, 8, 1, 3)
        image_mapping.create_matrix_vertical_index()
        #image_mapping.print_index()

        visual = Visual("/home/didier/deploy/visuals/tests/line.png", False)
        image_mapping.fill_image(self.pixels, visual.rgb)
        self.pixels.show()

        time.sleep(0.5)

    def test_24_16(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        image_mapping = ImageMapping(start_pixel=0, global_width=24, global_height=16, matrix_width=8, matrix_height=8, matrix_width_nb=3, matrix_height_nb=2)
        image_mapping.create_matrix_horizontal_index2()

        image_mapping.print_index()
        visual = Visual("/home/didier/deploy/visuals/tests/line.png", False)
        image_mapping.fill_image(self.pixels, visual.rgb)
        self.pixels.show()

    """def load_visual(self):
        visuals_path = self.json_manager.get_all_visual()
        for visual_path in visuals_path:
            self.visuals.append(Visual(visual_path[JsonManager.NAME], visual_path['path']))"""