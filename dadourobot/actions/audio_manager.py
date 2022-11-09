# pip3 install sound-player
# https://github.com/Krozark/sound-player/blob/master/example.py
import logging
import threading
from os.path import exists

from dadou_utils.misc import Misc
from dadou_utils.utils_static import KEY, NAME, PATH
from sound_player import Sound, SoundPlayer

from dadourobot.files.robot_json_manager import RobotJsonManager

from dadou_utils.audios.sound_object import SoundObject

from dadourobot.robot_static import AUDIOS_DIRECTORY


class AudioManager:

    player = SoundPlayer()
    silence = "audios/silence.wav"
    playlist = []
    current_audio = None
    current_audio_name = None

    def __init__(self, robot_json_manager:RobotJsonManager):
        self.json_manager = robot_json_manager

    def play_sounds_bak(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            self.player.enqueue(Sound(audio.get_path()), 1)
            for s in range(int(audio.get_time())):
                self.player.enqueue(Sound(self.silence), 1)
        self.player.play()

    def play_sound(self, audio):
        if exists(AUDIOS_DIRECTORY+audio[PATH]):
            self.current_audio = SoundObject(AUDIOS_DIRECTORY, audio[PATH])
            self.current_audio.play()
            self.current_audio_name = audio[PATH]
        else:
            logging.error("audio {} don't exist".format(audio[PATH]))

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

    def process(self, msg):
        if msg and hasattr(msg, KEY) and msg.key:
            logging.debug("number of thread : {}".format(threading.active_count()))
            audio_path = self.json_manager.get_audios(msg.key)
            if audio_path:
                if NAME in audio_path and audio_path[NAME] == 'stop':
                    self.stop_sound()
                    logging.info("stop sound")
                    return
                if audio_path[PATH] == self.current_audio_name and self.current_audio and self.current_audio.is_playing():
                    logging.debug("already playing {}".format(self.current_audio_name))
                    return
                else:
                    if not Misc.is_audio(AUDIOS_DIRECTORY + audio_path[PATH]):
                        logging.error("{} is not audio file".format(audio_path[PATH]))
                        return
                    if self.current_audio:
                        self.current_audio.stop()
                    self.current_audio_name = audio_path[PATH]
                    self.play_sound(audio_path)


            """           audio_sequence = self.json_manager.get_audio_seq(key)
            if audio_sequence:
                logging.info("play new audio")
                audios = []
                for audio_seq in audio_sequence[SEQUENCE]:
                    audio_path = self.json_manager.get_audio_path_by_name(audio_seq[NAME])
                    logging.debug("audios name : " + audio_seq[NAME] + " path : " + audio_path)
                    audios.append(PathTime(audio_path, audio_seq[DELAY]))

                self.play_sounds(audios)"""

