import logging
import logging.config
import os

import neopixel
from microcontroller import Pin
from dadou_utils.com.ws_server import WsMessage

from dadourobot.config import RobotConfig
from dadourobot.files.robot_json_manager import RobotJsonManager

from dadourobot.robot_static import RobotStatic
from dadou_utils.singleton import SingletonMeta


class RobotFactory(metaclass=SingletonMeta):

    def __init__(self):
        base_path = os.getcwd()
        logging_file = base_path+RobotStatic.LOGGING_CONFIG_FILE
        config_file = base_path+RobotStatic.CONFIG_FILE
        print(logging_file)
        logging.config.fileConfig(logging_file, disable_existing_loggers=False)

        self.robot_json_manager = RobotJsonManager(base_path, RobotStatic.JSON_DIRECTORY, RobotStatic.CONFIG_FILE)
        self.config = RobotConfig(self.robot_json_manager)
        self.ws_message = WsMessage()

        #TODO improve led lights
        #self.pixels = neopixel.NeoPixel(Pin(self.config.FACE_PIN), 512, auto_write=False, brightness=0.2)
        #self.pixels.brightness = 0.1

    def get_strip(self):
        return self.pixels

