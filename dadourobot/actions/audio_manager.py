# pip3 install sound-player
# https://github.com/Krozark/sound-player/blob/master/example.py
import logging
import threading
from os.path import exists

from dadou_utils.utils_static import AUDIO, AUDIOS_DIRECTORY, KEY, STOP, NAME, PATH, KEYS, JSON_AUDIOS, EXPRESSION, FACE, DURATION
from sound_player import Sound, SoundPlayer

from dadou_utils.misc import Misc
from dadou_utils.audios.sound_object import SoundObject

from dadourobot.input.global_receiver import GlobalReceiver


#TODO check : https://maelfabien.github.io/machinelearning/Speech8/#iv2a-noise-reduction

class AudioManager:

    player = SoundPlayer()
    silence = "audios/silence.wav"
    playlist = []
    current_audio = None
    current_audio_name = None

    def __init__(self, config, global_receiver, json_manager):
        self.config = config
        self.global_receiver = global_receiver
        self.json_manager = json_manager

    def play_sounds_bak(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            self.player.enqueue(Sound(audio.get_path()), 1)
            for s in range(int(audio.get_time())):
                self.player.enqueue(Sound(self.silence), 1)
        self.player.play()

    def play_sound(self, audio):
        if exists(self.config[AUDIOS_DIRECTORY]+audio):
        # TODO pb audio call 3 times / to improve
            if self.current_audio_name and audio in self.current_audio_name:
                return False
            if self.current_audio:
                self.current_audio.stop()
            self.current_audio = SoundObject(self.config[AUDIOS_DIRECTORY]+audio)

            #t = threading.Thread(target=self.current_audio.play)
            #t.start()

            self.current_audio.play()
            self.current_audio_name = audio
            return True
        else:
            logging.error("audio {} don't exist".format(self.config[AUDIOS_DIRECTORY]+audio))
            return False

    def play_sounds(self, audios):
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            if not self.current_audio_name in audio.get_path:
                sound = SoundObject(self.config[AUDIOS_DIRECTORY]+audio.get_path())
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

    def process(self):
        pass

    def update(self, msg):

        #TODO improve this part
        if msg and KEY in msg:
            logging.debug("number of thread : {}".format(threading.active_count()))
            audio_param = self.json_manager.get_element_from_key(self.config[JSON_AUDIOS], KEYS, msg[KEY])#self.json_manager.get_audios(msg[KEY])
            if audio_param:
                if audio_param and NAME in audio_param and audio_param[NAME] == STOP:
                    self.stop_sound()
                    logging.info("stop sound")
                    return
                if audio_param == self.current_audio_name and self.current_audio and self.current_audio.is_playing():
                    logging.debug("already playing {}".format(self.current_audio_name))
                    return
                else:
                    path = self.config[AUDIOS_DIRECTORY] + audio_param[NAME]
                    if not Misc.is_audio(path):
                        logging.error("{} is not audio file".format(path))
                        return
                    self.current_audio_name = audio_param[NAME]
                    self.play_sound(audio_param[NAME])

                    if EXPRESSION in audio_param:
                        face = audio_param[EXPRESSION]
                        duration = self.current_audio.duration * 1000
                        msg[DURATION] = duration
                        self.global_receiver.write_values({FACE: face, DURATION: duration})

        if msg and AUDIO in msg:
            if msg[AUDIO] == STOP:
                self.stop_sound()
                return
            if self.play_sound(msg[AUDIO]):
                self.current_audio_name = msg[AUDIO]
                if FACE in msg:
                    duration = self.current_audio.duration * 1000
                    msg[DURATION] = duration
                    self.global_receiver.write_values({DURATION: duration})

            del msg[AUDIO]
            self.global_receiver.write_msg(msg)

        return msg


