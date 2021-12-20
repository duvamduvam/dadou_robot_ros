import time
import unittest
from python.wheel import Wheel


class WheelTest(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
