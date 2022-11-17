from dadourobot.tests.conf_test import TestSetup
TestSetup()

from dadourobot.config import RobotConfig
from dadourobot.files.robot_json_manager import RobotJsonManager

import time
import unittest
from dadourobot.actions.audio_manager import AudioManager
from dadourobot.actions.vlc_audio import VlCAudio


class AudioTests(unittest.TestCase):
    json_manager = RobotJsonManager(RobotConfig.BASE_PATH)
    audio = AudioManager(json_manager)

    @unittest.skip
    def test_key_seq(self):
        self.audio.update("C1")
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

    def test_vlc3(self):
        json_manager = RobotJsonManager(RobotConfig.BASE_PATH)
        audiovlc = VlCAudio(json_manager)
        audiovlc.process("C1")
        time.sleep(1000)
