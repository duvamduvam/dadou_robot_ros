import json
import logging

import jsonpath_rw_ext

# '{}_{}_{}_{}'.format(s1, i, s2, f)
from dadou_utils.files.abstract_json_manager import AbstractJsonManager

from dadourobot.robot_static import RobotStatic


class RobotJsonManager(AbstractJsonManager):
    logging.info("start json manager")

    colors = None
    face_seq = None
    lights = None
    config = None
    lights_seq = None
    visual = None
    audios = None
    audio_seq = None

    def __init__(self, base_path, json_folder, config_file):
        super().__init__(base_path, json_folder, config_file)
        self.colors = self.open_json(RobotStatic.COLORS)
        self.face_seq = self.open_json(RobotStatic.FACE_SEQUENCE)
        self.lights = self.open_json(RobotStatic.LIGHTS)
        self.lights_seq = self.open_json(RobotStatic.LIGHTS_SEQUENCE)
        self.visual = self.open_json(RobotStatic.VISUALS)
        self.audios = self.open_json(RobotStatic.AUDIOS)
        self.audio_seq = self.open_json(RobotStatic.AUDIO_SEQUENCE)

    """@staticmethod
    def standard_return(result, return_first, attribut):
        # logging.debug(result)
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

        return None

    @staticmethod
    def find(json_data, iterate_key, expression):
        result = 0
        for seq in json_data[iterate_key]:
            if len(jsonpath_rw_ext.match(expression, seq)) > 0:
                result = seq
        return result"""

    def get_visual_path(self, key) -> str:
        result = jsonpath_rw_ext.match('$.visual[?name==' + key + ']', self.visual)
        return self.standard_return(result, True, 'path')

    def get_face_part(self, name) -> str:
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.face_seq)
        return self.standard_return(result, False, 'path')

    def get_all_visual(self):
        result = jsonpath_rw_ext.match('$.visual[*]', self.visual)
        return self.standard_return(result, False, False)

    def get_face_seq(self, key):
        result = self.find(self.face_seq, 'main_seq', '$.keys[?key ~ ' + key + ']')
        return self.standard_return(result, False, False)

    def get_part_seq(self, name):
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.face_seq)
        return self.standard_return(result, True, False)

    def get_lights(self, key):
        result = jsonpath_rw_ext.match('$.lights_seq[?keys~' + key + ']', self.lights_seq)
        # logging.debug(result)
        #return self.standard_return(result, True, key)
        return result[0]

    def get_color(self, key):
        result = jsonpath_rw_ext.match('$.colors[?name~' + key + ']', self.colors)
        logging.debug(result)
        if len(result) > 0:
            json_color = result[0][RobotStatic.COLOR]
            return (int(json_color['red']), int(json_color['green']), int(json_color['blue']))
        else:
            logging.error("no color" + key)
            return None

    def get_audio_seq(self, key):
        # logging.debug("key " + key)
        result = self.find(self.audio_seq, 'audios_seq', '$.keys[?key ~ ' + key + ']')
        return self.standard_return(result, False, key)

    @staticmethod
    def get_attribut(json_object, key):
        if key in json_object:
            return json_object[key]
        else:
            return None

    def get_audio_path_by_name(self, name) -> str:
        result = jsonpath_rw_ext.match('$.audios[?name~' + name + ']', self.audios)
        return self.standard_return(result, True, False)

    def get_audios(self, key: str) -> str:
        result = jsonpath_rw_ext.match('$.audios[?key~' + key + ']', self.audios)
        return self.standard_return(result, True, False)

    def get_config(self):
        return self.config

        """
        audios = []
        for seq in self.audio_sequence:
            logging.debug("iterate key : " + seq['key'])
            if seq['key'] == key:
                logging.debug("found key : " + key)
                for audio_seq in seq[JsonManager.SEQUENCE]:
                    audio_path = self.get_audio_path_by_name(audio_seq[JsonManager.NAME])
                    logging.debug("audios name : " + audio_seq[JsonManager.NAME] + " path : " + audio_path)
                    audios.append(PathTime(audio_path, audio_seq[JsonManager.DELAY]))
        return audios
        """
