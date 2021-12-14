#pip3 install sound-player
#https://github.com/Krozark/sound-player/blob/master/example.py
import logging
import time
import pygame

from threading import Thread
from sound_player import Sound, Playlist, SoundPlayer


class Audio:

    player = SoundPlayer()

    def play_sound(self, file):
        logging.info("play sound : " + file)
        self.player.stop()
        self.player.enqueue(Sound(file), 1)
        self.player.play()

    def stop_sound(self):
        self.player.stop()
