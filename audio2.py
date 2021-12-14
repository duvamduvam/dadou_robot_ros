#pip3 install sound-player
import logging
import time
import pygame

from threading import Thread
from sound_player import Sound, Playlist, SoundPlayer


class Audio2:
    pl = Playlist(concurency=2)

    @staticmethod
    def play_sound(self, file):
        self.pl.stop()
        logging.info("play sound : " + file)
        #sound = Sound(file)
        #sound.play()
        self.pl.enqueue(Sound(file))
        self.pl.play()
        time.sleep(10)
        time.sleep(3)

    @staticmethod
    def play(file):
        music_thread = Thread(target=Audio2.play_sound, args=[file])
        music_thread.start()
