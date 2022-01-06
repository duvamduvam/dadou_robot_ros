import unittest

import board
from adafruit_blinka.board.raspberrypi import raspi_4b

from python.config import Config
from python.tests.conf_test import TestSetup
from python.utils import Utils

TestSetup()


class TestConfig(unittest.TestCase):

    config = Config()

    def test_get_rpi_pins(self):
        print(board.__dict__)
        print(self.config.LIGHTS_PIN)