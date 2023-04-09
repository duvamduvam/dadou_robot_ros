# pip3 install sound-player
# https://github.com/Krozark/sound-player/blob/master/example.py
import logging
import vlc

#from sound_player import Sound, Playlist, SoundPlayer


from json_manager import JsonManager
from path_time import PathTime
from robot_factory import RobotFactory


class VlCAudio:


    silence = "audios/silence.wav"

    player = vlc.MediaPlayer(silence)

    def __init__(self):
        self.json_manager = RobotFactory().disk_json_manager

    def play_sounds(self, audios):
        self.player.stop()
        for audio in audios:
            logging.info("enqueue: " + audio.get_path())
            self.player = vlc.MediaPlayer(audio.get_path())
            #for s in range(int(audio.get_time())):
            #    self.player.enqueue(Sound(self.silence), 1)
        self.player.play()

    def stop_sound(self):
        self.player.stop()

    def process(self, key):
        if key:
            audio_sequence = self.json_manager.get_audio_seq(key)
            if audio_sequence:
                logging.info("play new audio")
                audios = []
                for audio_seq in audio_sequence[JsonManager.SEQUENCE]:
                    audio_path = self.json_manager.get_audio_path_by_name(audio_seq[JsonManager.NAME])
                    logging.debug("audios name : " + audio_seq[JsonManager.NAME] + " path : " + audio_path)
                    audios.append(PathTime(audio_path, audio_seq[JsonManager.DELAY]))

                self.play_sounds(audios)

