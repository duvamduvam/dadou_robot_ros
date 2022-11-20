# pip3 install sound-player
# https://github.com/Krozark/sound-player/blob/master/example.py
import logging
import threading
from os.path import exists

from dadou_utils.misc import Misc
from dadou_utils.utils_static import ANIMATION, AUDIO, KEY, NAME, PATH, KEYS, STOP, SPEAK, SPEAK_DURATION, TYPE
from sound_player import Sound, SoundPlayer

from dadourobot.actions.abstract_actions import ActionsAbstract
from dadourobot.files.robot_json_manager import RobotJsonManager

from dadou_utils.audios.sound_object import SoundObject

from dadourobot.robot_static import AUDIOS_DIRECTORY, JSON_AUDIOS


class AudioManager(ActionsAbstract):

    player = SoundPlayer()
    silence = "audios/silence.wav"
    playlist = []
    current_audio = None
    current_audio_name = None

    sequences_key = {}
    sequences_name = {}

    def __init__(self, robot_json_manager:RobotJsonManager):
        super().__init__(robot_json_manager, JSON_AUDIOS)

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
        if exists(AUDIOS_DIRECTORY+audio[NAME]):
            self.current_audio = SoundObject(AUDIOS_DIRECTORY, audio[NAME])
            self.current_audio.play()
            self.current_audio_name = audio[NAME]
            return self.current_audio.duration
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
            logging.info("stop sound")

    def update(self, msg):

        if msg and ANIMATION in msg.keys() and not msg[ANIMATION]:
            self.stop_sound()

        audio = self.get_sequence(msg, AUDIO)
        if not audio: return

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
            if self.current_audio:
                self.current_audio.stop()
            self.current_audio_name = audio[NAME]
            length = self.play_sound(audio)
            if TYPE in audio and audio[TYPE] == SPEAK:
                msg[SPEAK] = True
                msg[SPEAK_DURATION] = int(length*1000)
                return msg
