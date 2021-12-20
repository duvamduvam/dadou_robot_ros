import logging, json


class Mapping:

    def __init__(self):
        f = open('audio.json')
        self.audiodata = json.load(f)

    def get_audio_file(self, key: str) -> str:
        for audio in self.audiodata['audios']:
            if audio['key'] == key:
                logging.debug("getting audio mapping :" + audio['path'])
                return audio['path']
        logging.error("no audio for key : " + key)
