# pip3 install sound-player
# https://github.com/Krozark/sound-player/blob/master/example.py
import logging
import threading
from os.path import exists

from dadou_utils.misc import Misc
from dadou_utils.utils_static import AUDIO, KEY, NAME, PATH, KEYS, STOP
from sound_player import Sound, SoundPlayer

from dadourobot.files.robot_json_manager import RobotJsonManager

from dadou_utils.audios.sound_object import SoundObject

from dadourobot.robot_static import AUDIOS_DIRECTORY, JSON_AUDIOS


class AudioManager:

    player = SoundPlayer()
    silence = "audios/silence.wav"
    playlist = []
    current_audio = None
    current_audio_name = None

    audios_key = {}
    audios_name = {}

    def __init__(self, robot_json_manager:RobotJsonManager):
        self.json_manager = robot_json_manager
        self.load_sequences()

    def load_sequences(self):
        audio_list = self.json_manager.open_json(JSON_AUDIOS)
        for audio in audio_list:
            for key in audio[KEYS]:
                self.audios_key[key] = audio
            self.audios_name[audio[NAME]] = audio

    def play_sounds_bak(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            self.player.enqueue(Sound(audio.get_path()), 1)
            for s in range(int(audio.get_time())):
                self.player.enqueue(Sound(self.silence), 1)
        self.player.play()

    def play_sound(self, audio):
        if exists(AUDIOS_DIRECTORY+audio[NAME]):
            self.current_audio = SoundObject(AUDIOS_DIRECTORY, audio[NAME])
            self.current_audio.play()
            self.current_audio_name = audio[NAME]
        else:
            logging.error("audio {} don't exist".format(audio[NAME]))

    def play_sounds(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())

            sound = SoundObject(AUDIOS_DIRECTORY, audio.get_path())
            self.playlist.append(sound)
            #self.player.enqueue(Sound(audio.get_path()), 1)
            #for s in range(int(audio.get_time())):
            #    self.player.enqueue(Sound(self.silence), 1)
            sound.play()
        #self.player.play()

    def stop_sound(self):
        if self.current_audio:
            self.current_audio.stop()
            self.current_audio_name = ""

    def get_audio_from_input(self, msg):
        if not msg:
            return
        if KEY in msg and msg[KEY] in self.audios_key.keys():
            return self.audios_key[msg[KEY]]
        if AUDIO in msg  and msg[AUDIO] in self.audios_name.keys():
            return self.audios_name[msg[AUDIO]]

    def update(self, msg):

        audio_name = self.get_audio_from_input(msg)
        if not audio_name:
            return

        logging.debug("number of thread : {}".format(threading.active_count()))

        if audio_name[NAME] == STOP:
            self.stop_sound()
            logging.info("stop sound")
            return
        if audio_name[NAME] == self.current_audio_name and self.current_audio and self.current_audio.is_playing():
            logging.debug("already playing {}".format(self.current_audio_name))
            return
        else:
            if not Misc.is_audio(AUDIOS_DIRECTORY + audio_name[NAME]):
                logging.error("{} is not audio file".format(audio_name[NAME]))
                return
            if self.current_audio:
                self.current_audio.stop()
            self.current_audio_name = audio_name[NAME]
            self.play_sound(audio_name)

