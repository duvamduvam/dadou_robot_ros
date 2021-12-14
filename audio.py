#pip3 install sound-player
import logging
import time
import pygame

from threading import Thread
from sound_player import Sound, Playlist, SoundPlayer


class Audio:

    @staticmethod
    def play_sound(file):
        pl = Playlist(concurency=2)
        pl.stop()
        logging.info("play sound : " + file)
        pl.enqueue(Sound(file))
        pl.play()

    @staticmethod
    def play(file):
        music_thread = Thread(target=Audio.play_sound, args=[file])
        music_thread.start()
