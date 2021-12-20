#pip3 install sound-player
#https://github.com/Krozark/sound-player/blob/master/example.py
import logging

from mapping import Mapping
from sound_player import Sound, Playlist, SoundPlayer


class Audio:

    mapping = {}
    player = SoundPlayer()

    def __init__(self, mapping: Mapping):
        self.mapping = mapping

    def play_sound(self, file):
        logging.info("play sound : " + file)
        self.player.stop()
        self.player.enqueue(Sound(file), 1)
        self.player.play()

    def stop_sound(self):
        self.player.stop()

    def execute(self, key):
        audio_path = self.mapping.get_audio_file("A3")
        self.play_sound(audio_path)
