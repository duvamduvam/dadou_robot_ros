#pip3 install sound-player
import logging
import time
import pygame

from threading import Thread
from sound_player import Sound, Playlist, SoundPlayer


class Audio2:

    @staticmethod
    def play_sound(file):
        logging.info("play sound : " + file)
        sound = Sound(file)
        sound.play()
        time.sleep(3)

    @staticmethod
    def play(file):
        music_thread = Thread(target=Audio2.play_sound, args=[file])
        music_thread.start()
