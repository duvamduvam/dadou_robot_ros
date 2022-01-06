import unittest
import logging.config
import board

from python.config import Config
from python.tests.conf_test import TestSetup
from python.utils import Utils

TestSetup()


class TestConfig(unittest.TestCase):

    config = Config()

    def test_get_rpi_pins(self):
        logging.info(board.__dict__)
        logging.info(self.config.LIGHTS_PIN)
