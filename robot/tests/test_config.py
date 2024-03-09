import logging.config
import unittest

import board

from robot.input.global_receiver import GlobalReceiver
from robot.robot_config import config


class TestConfig(unittest.TestCase):

    def __init__(self):
        super().__init__()
        #robot_json_manager = RobotJsonManager(config)
        self.receiver = GlobalReceiver(config, None)

    def test_get_rpi_pins(self):
        logging.info(board.__dict__)
        logging.info(config.LIGHTS_PIN)
