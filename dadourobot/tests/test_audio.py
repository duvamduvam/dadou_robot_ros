import os

from playsound import playsound

from dadou_utils.utils_static import AUDIO, KEY, JSON_DIRECTORY, JSON_CONFIG, BASE_PATH, AUDIOS_DIRECTORY
from dadourobot.actions.audio_manager import AudioManager
import simpleaudio as sa
from dadourobot.files.robot_json_manager import RobotJsonManager


import time
import unittest

from dadourobot.input.global_receiver import GlobalReceiver
from dadourobot.robot_config import config
from dadourobot.sequences.animation_manager import AnimationManager


class AudioTests(unittest.TestCase):
    config[BASE_PATH] = config[BASE_PATH].replace("/dadourobot", "")
    config[AUDIOS_DIRECTORY] = config[AUDIOS_DIRECTORY].replace("/dadourobot", "")

    robot_json_manager = RobotJsonManager(config)
    receiver = GlobalReceiver(config, AnimationManager(config, robot_json_manager))
    audio = AudioManager(config, receiver, robot_json_manager)

    def test_key_seq(self):
        msg = {KEY: "A9"}
        self.audio.update(msg)
        time.sleep(1000)

    #TODO fix path pb
    def test_background_sound(self):
        msg = {AUDIO: "song/gig.wav"}
        self.audio.update(msg)
        print("audio lunched duration {}".format(self.audio.get_audio_length()))
        time.sleep(5)
        msg = {AUDIO: "aie.wav"}
        self.audio.update(msg)
        print("audio lunched duration {}".format(self.audio.get_audio_length()))
        time.sleep(5)
        self.audio.stop_sound()

    def test_simpleaudio(self):
        #sound_object = sa.WaveObject.from_wave_file("/home/dadou/Nextcloud/Didier/python/dadou_robot/audios/speak/aie.wav")
        #play_obj = sound_object.play()
        #play_obj.wait_done()
        playsound('/home/dadou/Nextcloud/Didier/python/dadou_robot/audios/speak/aie.wav', block=False)

    def test_load(self):
        self.audio.index_audios()

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
