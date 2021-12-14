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
        self.pl.stop()
        self.pl.enqueue(Sound(file))
        self.pl.play()

    def stop_sound(self):
        self.pl.stop()

    def play(self, file):
        if self.music_thread:
            self.music_thread.join()
        self.music_thread = Thread(target=Audio.play_sound, args=(self, file))
        self.music_thread.start()
