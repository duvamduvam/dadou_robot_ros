import unittest
from python.lights import Lights


class LightsTest(unittest.TestCase):

    lights = Lights()

    def test_random(self):
        self.lights.random()


if __name__ == '__main__':
    unittest.main()
