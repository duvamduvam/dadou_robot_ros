import unittest
from python.mapping import Mapping
from python.audio import Audio


class AudioTests(unittest.TestCase):
    mapping = Mapping()
    audio = Audio(mapping)

    def play(self):
        self.execute("A5")


if __name__ == '__main__':
    unittest.main()
