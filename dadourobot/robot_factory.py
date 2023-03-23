import logging
import logging.config
import os

import adafruit_pca9685
import board
import busio
import neopixel
from dadou_utils.com.serial_devices_manager import SerialDeviceManager
from microcontroller import Pin

from actions.audios import AudioManager
from actions.face import Face
from actions.relays import RelaysManager
#from actions.lights import Lights
from actions.lights import Lights
from actions.neck import Neck
from actions.wheel import Wheel
from dadourobot.actions.left_arm import LeftArm
from dadourobot.actions.right_arm import RightArm

from files.robot_json_manager import RobotJsonManager

from dadou_utils.singleton import SingletonMeta

from robot_config import I2C_ENABLED, LIGHTS_PIN, PWM_CHANNELS_ENABLED, DIGITAL_CHANNELS_ENABLED, DEVICES_LIST

from robot_config import LOGGING_CONFIG_FILE
from sequences.animation_manager import AnimationManager


class RobotFactory(metaclass=SingletonMeta):

    def __init__(self):

        logging.config.fileConfig(LOGGING_CONFIG_FILE, disable_existing_loggers=False)

        self.robot_json_manager = RobotJsonManager()
        self.device_manager = SerialDeviceManager(DEVICES_LIST)
        self.audio = AudioManager(self.robot_json_manager)
        self.left_arm = LeftArm()
        self.right_arm = RightArm()
        self.neck = Neck()
        self.wheel = Wheel()
        self.relays = RelaysManager(self.robot_json_manager)

        #TODO improve led lights
        self.pixels = neopixel.NeoPixel(LIGHTS_PIN, 782, auto_write=False, brightness=0.05, pixel_order=neopixel.GRB)

        """pixel_pin = board.D18
        num_pixels = 30
        ORDER = neopixel.GRB

        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
        )"""

        self.face = Face(self.robot_json_manager, self.pixels)
        self.lights = Lights(self.robot_json_manager, self.pixels)
        #self.neck = Neck(self.config)

        self.animation_manager = AnimationManager(self.robot_json_manager)

    #def get_strip(self):
    #    return self.pixels

    def get_audio(self):
        return self.audio
