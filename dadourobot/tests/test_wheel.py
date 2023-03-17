import time
import unittest

from dadou_utils.utils_static import WHEEL_LEFT, WHEEL_RIGHT

import dadourobot
from dadourobot.tests.conf_test import TestSetup


class WheelTest(unittest.TestCase):
    test_setup = TestSetup()
    wheel = test_setup.wheel

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
