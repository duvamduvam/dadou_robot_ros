import os

import adafruit_pcf8574
import board
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

    i2c = board.I2C()  # uses board.SCL and board.SDA
    pcf = adafruit_pcf8574.PCF8574(i2c)

    dir1 = pcf.get_pin(0)


    def test_run(self):

        for w in range(0, 5):
        #while True:
            self.wheel.update({WHEEL_LEFT:60, WHEEL_RIGHT:60})
            self.dir1.value = True
            time.sleep(5)
            self.wheel.update({WHEEL_LEFT:60, WHEEL_RIGHT:-60})
            self.dir1.value = False
            time.sleep(5)
            """self.wheel.update({WHEEL_LEFT:-45, WHEEL_RIGHT:-45})
            time.sleep(5)
            self.wheel.update({WHEEL_LEFT:45, WHEEL_RIGHT:45})
            time.sleep(5)
            self.wheel.update({WHEEL_LEFT:-70, WHEEL_RIGHT:1})
            time.sleep(5)
            self.wheel.update({WHEEL_LEFT:1, WHEEL_RIGHT:-70})
            time.sleep(5)
            self.wheel.update({WHEEL_LEFT:70, WHEEL_RIGHT:70})
            time.sleep(5)"""