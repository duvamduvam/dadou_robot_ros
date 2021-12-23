import logging
import json
from jsonpath_ng import jsonpath, parse

class Mapping:

    def __init__(self):
        f = open('audio.json')
        audio_data = json.load(f)

        f = open('sequences.json')
        audio_sequence = json.load(f)

    def get_audio_file(self, key: str) -> str:

        #jsonpath_expression = parse('audios.[*].id')
        with open("db.json", 'r') as json_file:
            json_data = json.load(json_file)


        for audio in self.audio_data['audios']:
            if audio['key'] == key:
                logging.debug("getting audio mapping :" + audio['path'])
                return audio['path']
        logging.error("no audio for key : " + key)

    #def get_audio_sequence(self, key: str) :

