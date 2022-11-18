import json
import logging

import jsonpath_rw_ext

# '{}_{}_{}_{}'.format(s1, i, s2, f)
from dadou_utils.files.abstract_json_manager import AbstractJsonManager
from dadou_utils.utils_static import COLOR

from dadourobot.robot_static import JSON_AUDIOS, JSON_AUDIO_SEQUENCE, JSON_COLORS, JSON_EXPRESSIONS, JSON_MAPPINGS, \
    JSON_VISUALS, JSON_LIGHTS


class RobotJsonManager(AbstractJsonManager):
    logging.info("start json manager")

    audios = None
    audio_seq = None
    colors = None
    config = None
    expressions = None
    lights = None
    lights_seq = None
    mappings = None
    visual = None

    def __init__(self, base_path, json_folder, config_file):
        super().__init__(base_path, json_folder, config_file)
        self.audios = self.open_json(JSON_AUDIOS)
        self.audio_seq = self.open_json(JSON_AUDIO_SEQUENCE)
        self.colors = self.open_json(JSON_COLORS)
        self.expressions = self.open_json(JSON_EXPRESSIONS)
        self.lights = self.open_json(JSON_LIGHTS)
        self.mappings = self.open_json(JSON_MAPPINGS)
        self.visual = self.open_json(JSON_VISUALS)

    def get_visual_path(self, key) -> str:
        result = jsonpath_rw_ext.match('$.visual[?name==' + key + ']', self.visual)
        return self.standard_return(result, True, 'path')

    def get_face_part(self, name) -> str:
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.expressions)
        return self.standard_return(result, False, 'path')

    def get_all_visual(self):
        result = jsonpath_rw_ext.match('$.visual[*]', self.visual)
        return self.standard_return(result, False, False)

    #def get_face_seq(self, key):
    #    result = self.find(self.face_seq, 'main_seq', '$.keys[?key ~ ' + key + ']')
    #    return self.standard_return(result, False, False)

    def get_face_seq(self, value):
        return self.get_dict_from_list(self.expressions, "keys", value)

    def get_part_seq(self, name):
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.expressions)
        return self.standard_return(result, True, False)

    def get_lights(self, key):
        return self.get_dict_from_list(self.lights, "keys", key)


    """def get_lights(self, key):
        result = jsonpath_rw_ext.match('$.lights_seq[?keys~' + key + ']', self.lights)
        # logging.debug(result)
        #return self.standard_return(result, True, key)
        if len(result) > 0:
            return result[0]"""

    def get_color(self, key):
        result = jsonpath_rw_ext.match('$.colors[?name~' + key + ']', self.colors)
        logging.debug(result)
        if len(result) > 0:
            json_color = result[0][COLOR]
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
        #result = jsonpath_rw_ext.match('$.audios[?key~' + key + ']', self.audios)
        if key:
            result = jsonpath_rw_ext.match("$.audios[?(keys[*]~'"+key+"')]", self.audios)
            return self.standard_return(result, True, False)
        else:
            logging.error("input str None")

    def get_mappings(self, key: str, mapping_type: str) -> str:
        if key:
            result = jsonpath_rw_ext.match("$."+mapping_type+"[?(keys[*]~'"+key+"')]", self.mappings)
            return self.standard_return(result, True, 'value')
        else:
            logging.error("input str None")

    def get_config(self):
        return self.config
