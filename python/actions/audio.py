#pip3 install sound-player
#https://github.com/Krozark/sound-player/blob/master/example.py
import logging

from python.mapping import Mapping
from sound_player import Sound, Playlist, SoundPlayer


class Audio:

    #TODO load
    sequences = []

    mapping = {}
    player = SoundPlayer()
    silence = "audios/silence.wav"

    def __init__(self, mapping: Mapping):
        self.mapping = mapping

    def play_sounds(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            #todo check second parameter
            #todo enqueue 1 second sample
            self.player.enqueue(Sound(audio.get_path()), 1)
            if(int(audio.get_time())>0):
                self.player.enqueue(Sound(self.silence, int(audio.get_time())))
            #self.player.enqueue(Sound("1 sec silence"), audio.get_time())
        self.player.play()

    def stop_sound(self):
        self.player.stop()

    def process(self, key):
        audio_path = self.mapping.get_audios(key)
        self.play_sounds(audio_path)
        logging.info("update")
