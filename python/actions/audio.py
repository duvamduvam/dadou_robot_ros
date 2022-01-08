# pip3 install sound-player
# https://github.com/Krozark/sound-player/blob/master/example.py
import logging

from sound_player import Sound, Playlist, SoundPlayer

from python.json_manager import JsonManager
from python.path_time import PathTime


class Audio:

    player = SoundPlayer()
    silence = "audios/silence.wav"

    def __init__(self, json_manager: JsonManager):
        self.json_manager = json_manager

    def play_sounds(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            self.player.enqueue(Sound(audio.get_path()), 1)
            for s in range(int(audio.get_time())):
                self.player.enqueue(Sound(self.silence), 1)
        self.player.play()

    def stop_sound(self):
        self.player.stop()

    def process(self, key):
        audio_sequence = self.json_manager.get_audio_seq(key)
        if audio_sequence:
            audios = []
            for audio_seq in audio_sequence[JsonManager.SEQUENCE]:
                audio_path = self.json_manager.get_audio_path_by_name(audio_seq[JsonManager.NAME])
                logging.debug("audios name : " + audio_seq[JsonManager.NAME] + " path : " + audio_path)
                audios.append(PathTime(audio_path, audio_seq[JsonManager.DELAY]))

            self.play_sounds(audios)

