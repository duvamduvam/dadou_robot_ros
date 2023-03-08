import logging.config
from tests import TestSetup
TestSetup()

from dadourobot import JsonManager
from dadourobot import ImageMapping
from dadourobot import Visual

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
            self.visuals.append(Visual(visual_path[JsonManager.NAME], visual_path['path']))