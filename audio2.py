import logging
import time
import pygame

from pygame import mixer
from threading import Thread


class Audio2:

    @staticmethod
    def play_sound(file):
        logging.info("play sound : "+file)
        mixer.init(44100, -16, 2, 2048)
        sound = mixer.Sound(file)
        sound.play()
        while mixer.music.get_busy():
            time.delay(100)

    @staticmethod
    def play(file):
        logging.info("play sound : "+file)
        pygame.init()
        mixer.init()
        sound = mixer.Sound(file)
        sound.play()
        #while mixer.music.get_busy():
        #    time.delay(100)
        #music_thread = Thread(target=Audio2.play_sound,  args=[file])
        #music_thread.start()
