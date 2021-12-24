#pip3 install sound-player
#https://github.com/Krozark/sound-player/blob/master/example.py
import logging

from python.mapping import Mapping
from sound_player import Sound, Playlist, SoundPlayer


class Audio:

    #TODO load
    sequences = []

    mapping = {}
    player = SoundPlayer()
    silence = "audios/silence.wav"

    def __init__(self, mapping: Mapping):
        self.mapping = mapping

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
        audio_path = self.mapping.get_audios(key)
        self.play_sounds(audio_path)
        logging.info("update")
