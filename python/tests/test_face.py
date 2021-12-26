import logging.config

from python.actions.face import Face
from python.tests.conf_test import TestSetup

import unittest


class MyTestCase(unittest.TestCase):

    face = Face()

    def test_img_mouth(self):
        logging.info(self.face.visuals[0])
