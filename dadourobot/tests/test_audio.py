import os

from dadou_utils.utils_static import AUDIO, KEY

from robot_static import JSON_DIRECTORY, JSON_CONFIG
from tests.conf_test import TestSetup
TestSetup()

from config import RobotConfig
from files.robot_json_manager import RobotJsonManager

import time
import unittest
from actions.audios import AudioManager


class AudioTests(unittest.TestCase):

    robot_json_manager = RobotJsonManager(os.getcwd(), "/.."+JSON_DIRECTORY, JSON_CONFIG)
    config = RobotConfig(robot_json_manager)
    audio = AudioManager(robot_json_manager, config)

    def test_key_seq(self):
        msg = {KEY: "A9"}
        self.audio.update(msg)
        time.sleep(1000)

    #TODO fix path pb
    def test_audio_cmd(self):
        msg = {AUDIO: "speak/et-des-robots.mp3"}
        self.audio.update(msg)

    """
    @unittest.skip
    def test_playsound(self):
        sound = input(Config.BASE_PATH + "audios/gig.wav")
        playsound(sound)
        time.sleep(10000)


    def test_vlc2(self):
        logging.info("test vlc play : " + Config.BASE_PATH + "audios/gig.wav")
        player = vlc.MediaPlayer(Config.BASE_PATH + "audios/gig.wav")
        player.play()
        while True:
            time.sleep(10)
                """
