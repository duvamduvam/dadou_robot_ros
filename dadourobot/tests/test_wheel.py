import time
import unittest

from dadourobot.actions.left_arm import LeftArm
from dadourobot.actions.right_arm import RightArm

from dadou_utils.utils_static import WHEEL_LEFT, WHEEL_RIGHT
from dadourobot.actions.wheel import Wheel
from dadourobot.robot_config import config
from dadourobot.tests.conf_test import TestSetup


class WheelTest(unittest.TestCase):
    test_setup = TestSetup()
    wheel = Wheel(config)
    left_arm = LeftArm(config)
    right_arm = RightArm(config)

    def test_run(self):

        for w in range(0, 5):
        #while True:
            self.wheel.update({WHEEL_LEFT: 60, WHEEL_RIGHT: 60})
            #self.dir1.value = True
            time.sleep(5)
            self.wheel.update({WHEEL_LEFT: -60, WHEEL_RIGHT: -60})
            #self.dir1.value = False
            time.sleep(5)
        self.wheel.stop()

    def test_wheel(self):

        for w in range(0, 5):
        #while True:
            self.wheel.update({WHEEL_LEFT: 60, WHEEL_RIGHT: 60})
            #self.dir1.value = True
            time.sleep(5)
            self.wheel.update({WHEEL_LEFT: -60, WHEEL_RIGHT: -60})
            #self.dir1.value = False
            time.sleep(5)
            self.wheel.update({WHEEL_LEFT: 0, WHEEL_RIGHT: 0})
            # self.dir1.value = False
            time.sleep(5)
        self.wheel.stop()
