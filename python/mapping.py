import logging
import json
from jsonpath_ng import jsonpath, parse

from python.path_time import PathTime


class Mapping:

    def __init__(self):
        f = open('audio.json')
        self.audio_data = json.load(f)

        f = open('audio_sequence.json')
        self.audio_sequence = json.load(f)

    def get_audio_path_by_name(self, name) -> str:
        for audio in self.audio_data:
            if audio['name'] == name:
                return audio['path']
        logging.error("no path for audio name : " + name)

    def get_audios(self, key: str) -> str:

        audios = []
        for seq in self.audio_sequence:
            logging.debug("iterate key : " + seq['key'])
            if seq['key'] == key:
                logging.debug("found key : " + key)
                for audio_seq in seq['sequence']:
                    audio_path = self.get_audio_path_by_name(audio_seq['name'])
                    logging.debug("audios name : " + audio_seq['name'] + " path : " + audio_path)
                    audios.append(PathTime(audio_path, audio_seq['wait']))
        return audios

