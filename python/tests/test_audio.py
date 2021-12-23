import logging
import logging.config
import time
import unittest
from python.mapping import Mapping
from python.audio import Audio


class AudioTests(unittest.TestCase):

    logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
    mapping = Mapping()
    audio = Audio(mapping)

    def test_play(self):
        self.audio.process("A5")
        time.sleep(20)
