import json
import logging

import jsonpath_rw_ext


class JsonManager:
    with open("json/face_sequence.json", 'r') as json_file:
        face_seq = json.load(json_file)

    with open("json/visual.json", 'r') as json_file:
        visual = json.load(json_file)

    def get_visual_path(self, key) -> str:
        result = jsonpath_rw_ext.match('$.visual[?name==' + key + ']', self.visual)
        if len(result) == 0:
            logging.error("no visual path for " + key)
            return
        logging.debug(result)
        return result[0]['path']

    def get_face_seq(self, key) -> str:
        result = jsonpath_rw_ext.match('$.face_seq[?name==' + key + ']', self.face_seq)
        if len(result) == 0:
            logging.error("no visual path for " + key)
            return
        logging.debug(result)
        return result[0]

    def get_all_visual(self):
        result = jsonpath_rw_ext.match('$.visual[*]', self.visual)
        logging.debug(result)
        return result
