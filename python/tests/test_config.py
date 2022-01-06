import unittest
import logging.config
import board

from python.config import MConfig
from python.json_manager import JsonManager
from python.tests.conf_test import TestSetup

TestSetup()


class TestConfig(unittest.TestCase):

    json_manager = JsonManager()
    config = MConfig(json_manager)

    def test_get_rpi_pins(self):
        logging.info(board.__dict__)
        logging.info(self.config.LIGHTS_PIN)
