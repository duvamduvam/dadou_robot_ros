import unittest
import logging.config
import board

from robot_config import Config
from dadourobot import JsonManager
from tests import TestSetup

TestSetup()


class TestConfig(unittest.TestCase):

    json_manager = JsonManager()
    config = Config(json_manager)

    def test_get_rpi_pins(self):
        logging.info(board.__dict__)
        logging.info(self.config.LIGHTS_PIN)
