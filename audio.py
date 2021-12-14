#pip3 install sound-player
import logging
import time
import pygame

from threading import Thread
from sound_player import Sound, Playlist, SoundPlayer


class Audio:
    pl = Playlist(concurency=2)

    @staticmethod
    def play_sound(self, file):
        self.pl.stop()
        logging.info("play sound : " + file)
        self.pl.enqueue(Sound(file))
        self.pl.play()

    @staticmethod
    def play(file):
        music_thread = Thread(target=Audio.play_sound, args=[file])
        music_thread.start()
