import os
import sys
import time
import unittest

from dadou_utils.audios.piano_player import PianoPlayer
from dadou_utils.utils_static import JSON_DIRECTORY, JSON_CONFIG, NOTE, BASE_PATH, AUDIOS_DIRECTORY
from dadourobot.files.robot_json_manager import RobotJsonManager
from dadourobot.robot_config import config


class TestPiano(unittest.TestCase):
    #config[BASE_PATH] = os.getcwd() + "/.."
    config[BASE_PATH] = config[BASE_PATH] + "/.."
    print(config[BASE_PATH])
    config[AUDIOS_DIRECTORY] = config[AUDIOS_DIRECTORY].replace('/dadourobot', '')

    robot_json_manager = RobotJsonManager(config)
    piano_player = PianoPlayer(robot_json_manager)

    def test_note(self):
        print("A")
        self.piano_player.process({NOTE: "A"})
        time.sleep(2)
        print("B")
        self.piano_player.process({NOTE: "B"})
        time.sleep(2)
        print("C")
        self.piano_player.process({NOTE: "C"})
        time.sleep(2)
