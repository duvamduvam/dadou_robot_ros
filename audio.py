import logging

from playsound import playsound
from threading import Thread


class Audio:

    @staticmethod
    def play_sound(file):
        logging.info("play "+file)
        playsound(file)

    @staticmethod
    def play(file):
        music_thread = Thread(target=Audio.play_sound,  args=[file])
        music_thread.start()
