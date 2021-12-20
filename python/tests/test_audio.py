import logging
import time
import unittest
from python.mapping import Mapping
from python.audio import Audio


class AudioTests(unittest.TestCase):
    logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
    mapping = Mapping()
    audio = Audio(mapping)

    def play(self):
        self.execute("A5")
        time.sleep(20)

if __name__ == '__main__':
    unittest.main()
