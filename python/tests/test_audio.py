import unittest
from python.audio import Audio


class AudioTests(unittest.TestCase):
    audio = Audio()

    def play(self):
        self.execute("A5")


if __name__ == '__main__':
    unittest.main()
