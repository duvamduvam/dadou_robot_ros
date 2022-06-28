from dadourobot.tests.conf_test import TestSetup
TestSetup()

import time
import unittest
from dadourobot.actions.wheel import Wheel


class WheelTest(unittest.TestCase):

    TestSetup()

    wheel = Wheel()

    def test_run(self):
        self.wheel.update("AA")
        self.wheel.process()
        time.sleep(1)
        self.wheel.process()
        time.sleep(1)
        self.wheel.process()
        time.sleep(1)
        self.wheel.process()
        time.sleep(1)
        self.wheel.process()

