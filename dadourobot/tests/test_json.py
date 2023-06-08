import logging.config
from tests.conf_test import TestSetup
from actions import Visual

TestSetup()

import json

import unittest
import jsonpath_rw_ext

from dadoucontrol import JsonManager

class TestJson(unittest.TestCase):

    json_manager = JsonManager()

    #def test_get_main_seq(self):
    #    result = self.json_manager.get_face_seq("A1")
    #    logging.info(result)

    @unittest.skip
    def test_json_path(self):
        with open("json/face_sequence.json", 'r') as json_file:
            json_data = json.load(json_file)
        list_val = jsonpath_rw_ext.match('$.face_seq[?name==speak]', json_data)
        print(list_val[0][JsonManager.SEQUENCE])
        #logging.error("test45")

    #@unittest.skip
    #def test_get_visual_path(self):
    #    result = self.json_manager.get_visual_path("mopen1")
    #    print(result)

    #@unittest.skip
    #def test_get_face_seq(self):
    #    result = self.json_manager.get_face_seq("speak")
    #    print(result)

    """@unittest.skip
    def test_get_all_visual(self):
        print("load all visual")
        visuals_path = self.json_manager.get_all_visual()
        for visual_path in visuals_path:
            self.visuals.append(Visual(visual_path[JsonManager.NAME], visual_path['path']))

        result = self.json_manager.get_all_visual()
        print(result)"""
