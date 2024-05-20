import logging

from dadou_utils_ros.files.abstract_json_manager import AbstractJsonManager
from dadou_utils_ros.utils_static import JSON_AUDIOS, JSON_COLORS, JSON_EXPRESSIONS, JSON_LIGHTS, JSON_RELAYS, JSON_NOTES, \
    JSON_AUDIOS_DATAS
from dadou_utils_ros.utils_static import JSON_LIGHTS_BASE

from robot.robot_config import config

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
    relays = None
    visual = None

    def __init__(self, config):
        self.config = config
        component = [self.config[JSON_AUDIOS], self.config[JSON_COLORS], self.config[JSON_EXPRESSIONS],\
                self.config[JSON_LIGHTS], config[JSON_LIGHTS_BASE], self.config[JSON_RELAYS], self.config[JSON_NOTES], self.config[JSON_AUDIOS_DATAS]]

        super().__init__(config, component)
        #super().__init__( self.config[JSON_DIRECTORY])
        #self.audios = self.open_json(self.config[JSON_AUDIOS])
        #self.audio_seq = self.open_json(self.config[JSON_AUDIO_SEQUENCE])
        #self.colors = self.open_json(self.config[JSON_COLORS])
        #self.expressions = self.open_json(self.config[JSON_EXPRESSIONS])
        #self.lights = self.open_json(self.config[JSON_LIGHTS])
        #self.mappings = self.open_json(self.config[JSON_MAPPINGS])
        #self.relays = self.open_json(self.config[JSON_RELAYS])
        #self.visual = self.open_json(self.config[JSON_VISUALS])

    #def get_visual_path(self, key) -> str:
    #    result = jsonpath_rw_ext.match('$.visual[?name==' + key + ']', self.json_files[self.config[JSON_VISUALS]])
    #    return self.standard_return(result, True, 'path')

    #def get_face_part(self, name) -> str:
    #    result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.json_files[self.config[JSON_EXPRESSIONS]])
    #    return self.standard_return(result, False, 'path')

    #def get_all_visual(self):
    #    result = jsonpath_rw_ext.match('$.visual[*]', self.json_files[self.config[JSON_RELAYS]])
    #    return self.standard_return(result, False, False)

    #def get_face_seq(self, key):
    #    result = self.find(self.face_seq, 'main_seq', '$.keys[?key ~ ' + key + ']')
    #    return self.standard_return(result, False, False)

    #def get_face_seq(self, value):
    #    return self.get_dict_from_list(self.json_files[self.config[JSON_EXPRESSIONS]], "keys", value)

    """def get_part_seq(self, name):
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.json_files[self.config[JSON_EXPRESSIONS]])
        return self.standard_return(result, True, False)"""

    #def get_lights(self, key):
    #    return self.get_dict_from_list(self.json_files[self.config[JSON_LIGHTS]], "keys", key)


    """def get_lights(self, key):
        result = jsonpath_rw_ext.match('$.lights_seq[?keys~' + key + ']', self.lights)
        # logging.debug(result)
        #return self.standard_return(result, True, key)
        if len(result) > 0:
            return result[0]"""

    """def get_color(self, key):
        result = jsonpath_rw_ext.match('$.colors[?name~' + key + ']', self.json_files[self.config[JSON_COLORS]])
        logging.debug(result)
        if len(result) > 0:
            json_color = result[0][COLOR]
            return (int(json_color['red']), int(json_color['green']), int(json_color['blue']))
        else:
            logging.error("no color" + key)
            return None"""

    #def get_audio_seq(self, key):
    #    # logging.debug("key " + key)
    #    result = self.find(self.json_files[self.config[JSON_AUDIO_SEQUENCE]], 'audios_seq', '$.keys[?key ~ ' + key + ']')
    #    return self.standard_return(result, False, key)

    #def get_audio_path_by_name(self, name) -> str:
    #    result = jsonpath_rw_ext.match('$.audios[?name~' + name + ']', self.json_files[self.config[JSON_AUDIOS]])
    #    return self.standard_return(result, True, False)

    """def get_audios(self, key: str) -> str:
        #result = jsonpath_rw_ext.match('$.audios[?key~' + key + ']', self.audios)
        if key:
            result = jsonpath_rw_ext.match("$.audios[?(keys[*]~'"+key+"')]", self.json_files[self.config[JSON_AUDIOS]])
            return self.standard_return(result, True, False)
        else:
            logging.error("input str None")"""

    """def get_mappings(self, key: str, mapping_type: str) -> str:
        if key:
            result = jsonpath_rw_ext.match("$."+mapping_type+"[?(keys[*]~'"+key+"')]", self.json_files[self.config[JSON_MAPPINGS]])
            return self.standard_return(result, True, 'value')
        else:
            logging.error("input str None")"""

    """def get_relay(self, input_key: str):
        if input_key:
            for key, values in self.json_files[self.config[JSON_RELAYS]].items():
                if input_key in values:
                    return key
        else:
            logging.error("input str None")"""

    #def get_config(self):
    #    return self.config
