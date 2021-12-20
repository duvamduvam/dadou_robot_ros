import time
import unittest
from python.lights import Lights


class LightsTest(unittest.TestCase):
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)

    lights = Lights()

    def test_random(self):
        for i in range(100):
            self.lights.random()
            time.sleep(1)

    def test_full_color(self):
        self.lights.fill(self.BLUE)
        time.sleep(10)

if __name__ == '__main__':
    unittest.main()
