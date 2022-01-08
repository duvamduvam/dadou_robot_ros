#pip3 install sound-player
#https://github.com/Krozark/sound-player/blob/master/example.py
import logging

from sound_player import Sound, Playlist, SoundPlayer

from python.json_manager import JsonManager
from python.path_time import PathTime


class Audio:

    #TODO load
    sequences = []

    mapping = {}
    player = SoundPlayer()
    silence = "audios/silence.wav"

    def __init__(self, json_manager: JsonManager):
        self.json_manager = json_manager

    def play_sounds(self, audios):
        self.player.stop()

        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            self.player.enqueue(Sound(audio.get_path()), 1)
            for s in range(int(audio.get_time())):
                self.player.enqueue(Sound(self.silence), 1)
        self.player.play()

    def stop_sound(self):
        self.player.stop()

    def process(self, key):
        audio_sequence = self.json_manager.get_audios(key)
        if audio_sequence:
            audios = []
            for seq in audio_sequence:
                logging.debug("iterate key : " + seq['key'])
                if seq['key'] == key:
                    logging.debug("found key : " + key)
                    for audio_seq in seq['sequence']:
                        audio_path = self.get_audio_path_by_name(audio_seq['name'])
                        logging.debug("audios name : " + audio_seq['name'] + " path : " + audio_path)
                        audios.append(PathTime(audio_path, audio_seq['wait']))

            self.play_sounds(audios)
            logging.info("update")
