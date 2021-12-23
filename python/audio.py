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

    def __init__(self, mapping: Mapping):
        self.mapping = mapping

    def play_sounds(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.path)
            #todo check second parameter
            #todo enqueue 1 second sample
            self.player.enqueue(Sound(audio.path), 1)
            self.player.enqueue(Sound("1 sec silence"), audio.time)
        self.player.play()

    def stop_sound(self):
        self.player.stop()

    def update(self):
        logging.info("update")



class PathTime:

    path = {}
    time = 0

    def path(self) -> str:
        return self.path

    def time(self) -> int:
        return self.time
