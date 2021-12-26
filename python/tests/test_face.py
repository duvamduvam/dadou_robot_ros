import logging.config
import time

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
        #self.face.pixels[0] = visual.rgb[0]
        logging.info("test 1 pixel")
        logging.info(visual.rgb[0])
        #self.face.fill_matrix(0, 64, visual)
        #self.face.pixels.show()
        time.sleep(100)
        #logging.info(visual.rgb)
