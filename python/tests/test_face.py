import logging.config

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

    def test_img_mouth(self):
        logging.info("test face")
        logging.info(self.face.visuals[0].rgb)
        path = self.json_manager.get_visual_path("eye-still")
        visual = Visual("eye-still", path)
        logging.info(visual.rgb)
