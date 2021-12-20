import time
import unittest
from python.lights import Lights


class LightsTest(unittest.TestCase):

    lights = Lights()

    def test_random(self):
        for i in range(100):
            self.lights.random()
            time.sleep(1)

if __name__ == '__main__':
    unittest.main()
