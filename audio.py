#pip3 install sound-player
#https://github.com/Krozark/sound-player/blob/master/example.py
import logging
import time
import pygame

from threading import Thread
from sound_player import Sound, Playlist, SoundPlayer


class Audio:

    music_thread = {}
    pl = Playlist(concurency=2)
    player = SoundPlayer()

    def play_sound(self, file):
        logging.info("play sound : " + file)
        self.pl = Playlist(concurency=2)
        self.pl.stop()
        self.pl.enqueue(Sound(file))
        self.pl.play()

    def play_sound2(self, file):
        logging.info("play sound : " + file)
        self.player.stop()
        self.player = SoundPlayer()
        # first player
        self.player.enqueue(Sound(file), 1)
        self.player.play()

    def stop_sound(self):
        self.pl.stop()

    def play(self, file):
        if self.music_thread:
            self.music_thread.join()
        self.music_thread = Thread(target=Audio.play_sound, args=(self, file))
        self.music_thread.start()
