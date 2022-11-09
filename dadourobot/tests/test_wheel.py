import os

from dadou_utils.utils_static import WHEEL_LEFT, WHEEL_RIGHT

from dadourobot.config import RobotConfig
from dadourobot.files.robot_json_manager import RobotJsonManager
from dadourobot.robot_static import JSON_DIRECTORY, JSON_CONFIG
from dadourobot.tests.conf_test import TestSetup
TestSetup()

import time
import unittest
from dadourobot.actions.wheel import Wheel


class WheelTest(unittest.TestCase):

    TestSetup()
    base_path = os.getcwd()
    robot_json_manager = RobotJsonManager('/home/didier/deploy/', 'json/', JSON_CONFIG)
    config = RobotConfig(robot_json_manager)

    wheel = Wheel(config)

    def test_run(self):

        #for w in range(0, 100):
        self.wheel.update({WHEEL_LEFT:-70, WHEEL_RIGHT:-70})
        time.sleep(5)
        self.wheel.update({WHEEL_LEFT:70, WHEEL_RIGHT:70})
        time.sleep(5)
        self.wheel.update({WHEEL_LEFT:-70, WHEEL_RIGHT:1})
        time.sleep(5)
        self.wheel.update({WHEEL_LEFT:1, WHEEL_RIGHT:-70})
        time.sleep(5)
        self.wheel.update({WHEEL_LEFT:70, WHEEL_RIGHT:70})
        time.sleep(5)