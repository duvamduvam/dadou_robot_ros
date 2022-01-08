import logging.config

from python.json_manager import JsonManager
from python.tests.conf_test import TestSetup
TestSetup()
import logging.config
import time
import unittest
from python.actions.audio import Audio
from python.path_time import PathTime



class AudioTests(unittest.TestCase):

    json_manager = JsonManager()
    audio = Audio(json_manager)

    def test_key_seq(self):
        self.audio.process("C1")
        time.sleep(20)
