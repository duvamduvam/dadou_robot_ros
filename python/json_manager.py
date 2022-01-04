import json
import logging

import jsonpath_rw_ext


class JsonManager:
    logging.info("start json manager")

    COLOR = 'color'
    DURATION = 'duration'
    METHOD = 'meethod'
    NAME = 'name'
    KEYS = 'keys'
    LOOP = 'loop'


    JSON_PATH = "json/"
    AUDIOS = "audios.json"
    AUDIO_SEQUENCE = "audio_sequence.json"
    COLORS = "colors.json"
    FACE_SEQUENCE = "face_sequence.json"
    LIGHTS = "lights.json"
    LIGHTS_SEQUENCE = "lights_sequence.json"
    VISUALS = "visuals.json"

    with open(JSON_PATH + COLORS, 'r') as json_file:
        colors = json.load(json_file)

    with open(JSON_PATH + FACE_SEQUENCE, 'r') as json_file:
        face_seq = json.load(json_file)

    with open(JSON_PATH + LIGHTS, 'r') as json_file:
        lights = json.load(json_file)

    with open(JSON_PATH + LIGHTS_SEQUENCE, 'r') as json_file:
        lights_seq = json.load(json_file)

    with open(JSON_PATH + VISUALS, 'r') as json_file:
        visual = json.load(json_file)

    with open(JSON_PATH + AUDIOS) as json_file:
        audios = json.load(json_file)

    with open(JSON_PATH + AUDIO_SEQUENCE) as json_file:
        audio_seq = json.load(json_file)

    @staticmethod
    def standard_return(result, return_first, input_key, attribut, json_file):
        logging.debug(result)
        to_return = {}
        error = False

        if not bool(result):
            error = True
        else:
            if return_first:
                if len(result) > 0:
                    to_return = result[0]
                else:
                    error = True
            else:
                to_return = result
            if attribut:
                to_return = to_return[attribut]

        if not error:
            return to_return
        else:
            logging.error("no data for " + input_key + " in " + json_file)
        return 0

    def get_visual_path(self, key) -> str:
        result = jsonpath_rw_ext.match('$.visual[?name==' + key + ']', self.visual)
        return self.standard_return(result, True, key, 'path', self.VISUALS)

    def get_face_part(self, name) -> str:
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.face_seq)
        return self.standard_return(result, False, name, 'path', self.FACE_SEQUENCE)

    def get_all_visual(self):
        result = jsonpath_rw_ext.match('$.visual[*]', self.visual)
        return self.standard_return(result, False, False, False, self.VISUALS)

    def get_face_seq(self, key):
        result = jsonpath_rw_ext.match('$.main_seq[?keys~\"' + key + '\"]', self.face_seq)
        return self.standard_return(result, True, key, False, self.FACE_SEQUENCE)

    def get_part_seq(self, name):
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.face_seq)
        return self.standard_return(result, True, name, False, self.FACE_SEQUENCE)

    def get_lights(self, key):
        result = jsonpath_rw_ext.match('$.lights_seq[?keys~' + key + ']', self.lights_seq)
        logging.debug(result)
        return self.standard_return(result, True, key, False, self.LIGHTS_SEQUENCE)

    def get_color(self, key):
        result = jsonpath_rw_ext.match('$.colors[?name~' + key + ']', self.colors)
        logging.debug(result)
        if len(result) > 0:
            json_color = result[0][JsonManager.COLOR]
            return (int(json_color['red']), int(json_color['green']), int(json_color['blue']))
        else:
            logging.error("no color" + key)
            return 0

    @staticmethod
    def get_attribut(json_object, key):
        if key in json_object:
            return json_object[key]
        else:
            logging.error("no attribut" + key)
            return 0

    def get_audio_path_by_name(self, name) -> str:
        result = jsonpath_rw_ext.match('$.audios[?name~' + name + ']', self.audios)
        return self.standard_return(result, True, False, self.AUDIOS)

    def get_audios(self, key: str) -> str:
        result = jsonpath_rw_ext.match('$.audios_seq[?name~' + key + ']', self.audios)
        return self.standard_return(result, True, False, self.AUDIO_SEQUENCE)

        """
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
        """
