import logging.config
from python.tests.conf_test import TestSetup
TestSetup()

from python.actions.face import Face
from python.tests.conf_test import TestSetup

import unittest


class MyTestCase(unittest.TestCase):

    face = Face()

    def test_img_mouth(self):
        print("test face")
        logging.info("test face")
        logging.info(self.face.visuals[0].rgb)
