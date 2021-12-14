#pip3 install sound-player
import logging
import time
import pygame

from threading import Thread
from sound_player import Sound, Playlist, SoundPlayer


class Audio:

    music_thread = {}

    @staticmethod
    def play_sound(file):
        pl = Playlist(concurency=2)
        pl.stop()
        logging.info("play sound : " + file)
        pl.enqueue(Sound(file))
        pl.play()

    @staticmethod
    def play(self, file):
        if self.music_thread:
            logging.info("play sound : " + file)
            self.music_thread.join()
        else:
            self.music_thread = Thread(target=Audio.play_sound, args=[file])
            self.music_thread.start()
