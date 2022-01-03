import json
import logging
import traceback

import jsonpath_rw_ext


class JsonManager:
    with open("json/colors.json", 'r') as json_file:
        colors = json.load(json_file)

    with open("json/face_sequence.json", 'r') as json_file:
        face_seq = json.load(json_file)

    with open("json/lights_sequence.json", 'r') as json_file:
        lights = json.load(json_file)

    with open("json/visual.json", 'r') as json_file:
        visual = json.load(json_file)

    def get_visual_path(self, key) -> str:
        result = jsonpath_rw_ext.match('$.visual[?name==' + key + ']', self.visual)
        if len(result) == 0:
            logging.error("no visual path for " + key)
            return
        logging.debug(result)
        return result[0]['path']

    def get_face_part(self, name) -> str:
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.face_seq)
        if len(result) == 0:
            logging.error("no visual path for " + name)
            return
        logging.debug(result)
        return result[0]

    def get_all_visual(self):
        result = jsonpath_rw_ext.match('$.visual[*]', self.visual)
        logging.debug(result)
        return result

    def get_face_seq(self, key):
        result = jsonpath_rw_ext.match('$.main_seq[?keys~' + key + ']', self.face_seq)
        logging.debug(result)
        return result[0]

    def get_part_seq(self, name):
        result = jsonpath_rw_ext.match('$.part_seq[?name==' + name + ']', self.face_seq)
        logging.debug(result)
        return result[0]

    def get_lights(self, key):
        result = jsonpath_rw_ext.match('$.lights_seq[?keys~' + key + ']', self.lights)
        logging.debug(result)
        if len(result) > 0:
            return result[0]
        return 0

    def get_color(self, key):
        result = jsonpath_rw_ext.match('$.colors[?name~' + key + ']', self.colors)
        logging.debug(result)
        json_color = result[0]['color']
        color = (int(json_color['red']), int(json_color['green']), int(json_color['blue']))
        return color

    @staticmethod
    def get_attribut(self, json_object, key):
        if key in json_object:
            return json_object[key]
        else:
            return {}
