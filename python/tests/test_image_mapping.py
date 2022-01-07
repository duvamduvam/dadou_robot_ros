import logging.config
from python.tests.conf_test import TestSetup
TestSetup()

from python.json_manager import JsonManager
from python.visual.image_mapping import ImageMapping
from python.visual.visual import Visual

import unittest


class TestImageMapping(unittest.TestCase):

    json_manager = JsonManager()
    logging.info("start image mapping test")
    image_mapping = ImageMapping(8, 8, 3, 2)
    visuals = []

    def test_something(self):
        strip = []
        self.load_visual()
        visual = Visual.get_visual("mopen1", self.visuals)
        self.image_mapping.mapping(strip, visual.rgb)

    def load_visual(self):
        visuals_path = self.json_manager.get_all_visual()
        for visual_path in visuals_path:
            self.visuals.append(Visual(visual_path['name'], visual_path['path']))