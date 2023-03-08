# pip3 install sound-player
# https://github.com/Krozark/sound-player/blob/master/example.py
import logging
import threading
from os.path import exists

from dadou_utils.misc import Misc
from dadou_utils.utils_static import ANIMATION, AUDIO, NAME, STOP, FACE, \
    LIGHTS
from sound_player import Sound, SoundPlayer

from actions.abstract_actions import ActionsAbstract
from files.robot_json_manager import RobotJsonManager

from dadou_utils.audios.sound_object import SoundObject

from robot_static import AUDIOS_DIRECTORY, JSON_AUDIOS, LOOP_DURATION
from dadou_utils.utils_static import EXPRESSION

class AudioManager(ActionsAbstract):

    player = SoundPlayer()
    silence = "audios/silence.wav"
    playlist = []
    current_audio = None
    current_audio_name = None

    sequences_key = {}
    sequences_name = {}

    def __init__(self, robot_json_manager:RobotJsonManager, config):
        super().__init__(robot_json_manager, config, JSON_AUDIOS)

    #def load_sequences(self):
    #    audio_list = self.json_manager.open_json(JSON_AUDIOS)
    #    for audio in audio_list:
    #        for key in audio[KEYS]:
    #            self.sequences_key[key] = audio
    #        self.sequences_name[audio[NAME]] = audio

    def play_sounds_bak(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            self.player.enqueue(Sound(audio.get_path()), 1)
            for s in range(int(audio.get_time())):
                self.player.enqueue(Sound(self.silence), 1)
        self.player.play()

    def play_sound(self, audio):
        if exists(AUDIOS_DIRECTORY+audio):
            self.stop_sound()
            self.current_audio = SoundObject(AUDIOS_DIRECTORY, audio)
            self.current_audio.play()
            self.current_audio_name = audio
            return self.current_audio.duration
        else:
            logging.error("audio {} don't exist".format(audio))

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
            logging.info("stop sound")

    #TODO improve audio[NAME] // msg[AUDIO]
    def update(self, msg):
        if msg and AUDIO in msg:
            if msg[AUDIO] == STOP:
                self.stop_sound()
                return
            if msg[AUDIO] == self.current_audio_name and self.current_audio and self.current_audio.is_playing():
                logging.debug("already playing {}".format(self.current_audio_name))
                return
            length = self.play_sound(msg[AUDIO])
            msg[LOOP_DURATION] = int(length * 1000)
            return

        if msg and ANIMATION in msg.keys() and not msg[ANIMATION]:
            self.stop_sound()

        audio = self.get_sequence(msg, AUDIO, False)
        if not audio : return

        logging.debug("number of thread : {}".format(threading.active_count()))

        if audio[NAME] == STOP:
            self.stop_sound()
            return
        if audio[NAME] == self.current_audio_name and self.current_audio and self.current_audio.is_playing():
            logging.debug("already playing {}".format(self.current_audio_name))
            return
        else:
            if not Misc.is_audio(AUDIOS_DIRECTORY + audio[NAME]):
                logging.error("{} is not audio file".format(audio[NAME]))
                return
            length = self.play_sound(audio[NAME])
            if EXPRESSION in audio or LIGHTS in audio:
                msg[LOOP_DURATION] = int(length*1000)
                if EXPRESSION in audio:
                    msg[FACE] = audio[EXPRESSION]
                if LIGHTS in audio:
                    msg[LIGHTS] = audio[LIGHTS]
                return msg
