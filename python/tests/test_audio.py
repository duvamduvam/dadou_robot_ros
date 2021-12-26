import logging.config
from python.tests.conf_test import TestSetup
TestSetup()
import logging.config
import time
import unittest
from python.mapping import Mapping
from python.actions.audio import Audio
from python.path_time import PathTime



class AudioTests(unittest.TestCase):

    mapping = Mapping()
    audio = Audio(mapping)

    def play(self):
        path_time = []
        path_time.append(PathTime("audios/lunettes.wav", 0))
        path_time.append(PathTime("audios/manteau.wav", 5))
        path_time.append(PathTime("audios/neverDie.wav", 1))
        self.audio.play_sounds(path_time)
        time.sleep(20)

    def test_key_seq(self):
        self.audio.process("A1")
        time.sleep(20)
