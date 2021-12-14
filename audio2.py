import logging

import pygame
from threading import Thread


class Audio2:

    @staticmethod
    def play_sound(file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    @staticmethod
    def play(file):
        music_thread = Thread(target=Audio2.play_sound,  args=[file])
        music_thread.start()
