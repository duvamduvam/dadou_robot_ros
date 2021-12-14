import logging

from pygame import mixer
from threading import Thread


class Audio2:

    @staticmethod
    def play_sound(file):
        #mixer.pre_init(44100, 16, 2, 4096)
        mixer.init()
        sound = mixer.Sound(file)
        sound.play()
        while mixer.music.get_busy():
            continue

    @staticmethod
    def play(file):
        music_thread = Thread(target=Audio2.play_sound,  args=[file])
        music_thread.start()
