#pip3 install sound-player
import logging
import time
import pygame

from threading import Thread
from sound_player import Sound, Playlist, SoundPlayer


class Audio:

    music_thread = {}
    pl = Playlist(concurency=2)

    def play_sound(self, file):
        logging.info("play sound : " + file)
        self.pl.enqueue(Sound(file))
        self.pl.play()

    def play(self, file):
        self.pl.stop()
        self.music_thread = Thread(target=Audio.play_sound, args=(self, file))
        self.music_thread.start()
