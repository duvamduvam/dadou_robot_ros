import os

from dadou_utils.utils_static import KEY

from dadourobot.robot_static import JSON_DIRECTORY, JSON_CONFIG
from dadourobot.tests.conf_test import TestSetup
TestSetup()

from dadourobot.config import RobotConfig
from dadourobot.files.robot_json_manager import RobotJsonManager

import time
import unittest
from dadourobot.actions.audios import AudioManager


class AudioTests(unittest.TestCase):

    robot_json_manager = RobotJsonManager(os.getcwd(), "/.."+JSON_DIRECTORY, JSON_CONFIG)
    config = RobotConfig(robot_json_manager)
    audio = AudioManager(robot_json_manager, config)

    def test_key_seq(self):
        msg = {KEY: "A9"}
        self.audio.update(msg)
        time.sleep(1000)

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
