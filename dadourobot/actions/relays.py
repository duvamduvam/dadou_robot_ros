import logging

import adafruit_pcf8574
import board

from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import KEY, I2C_ENABLED, DIGITAL_CHANNELS_ENABLED


class RelaysManager:

    OCTAVER = "octaver"
    HF_RECEIVER = "hf_receiver"
    EFFECT = "effect_on"
    VOICE_OUT = "voice_out"

    NORMAL_VOICE = "normal_voice"
    PITCHED_VOICE = "pitched_voice"

    def __init__(self, config, receiver, json_manager):

        self.receiver = receiver
        self.config = config
        if not self.config[I2C_ENABLED] or not self.config[DIGITAL_CHANNELS_ENABLED]:
            logging.warning("i2c digital disabled")
            return

        self.json_manager = json_manager

        i2c = board.I2C()  # uses board.SCL and board.SDA
        pcf = adafruit_pcf8574.PCF8574(i2c, address=0x21)

        self.power_hf = pcf.get_pin(3)
        self.power_hf.value = True
        self.power_effect = pcf.get_pin(2)
        self.power_effect.value = True
        self.effect = pcf.get_pin(1)
        self.effect.value = True
        self.voice_out = pcf.get_pin(0)
        self.voice_out.value = True

        self.last_effect_time = 0
        self.effect_timeout = 800

    def update(self, msg):

        if not self.config[I2C_ENABLED] or not self.config[DIGITAL_CHANNELS_ENABLED]:
            return msg

        if msg and KEY in msg:
            relay = self.json_manager.get_relay(msg[KEY])

            if relay == self.PITCHED_VOICE:
                self.voice_out.value = False
                self.effect.value = True
                self.last_effect_time = TimeUtils.current_milli_time()
                logging.info("switch effect on")

            if relay == self.NORMAL_VOICE:
                self.voice_out.value = False
                self.effect.value = False
                self.last_effect_time = TimeUtils.current_milli_time()
                logging.info("switch effect on")

            if relay == self.OCTAVER:
                self.power_effect.value = not self.power_effect.value
                logging.info("switch octaver {}".format(self.power_effect.value))

            if relay == self.HF_RECEIVER:
                self.power_hf.value = not self.power_hf.value
                logging.info("switch hf receiver {}".format(self.power_hf.value))

            if relay == self.EFFECT:
                #self.effect.value = True
                self.voice_out.value = False
                self.last_effect_time = TimeUtils.current_milli_time()
                logging.info("switch effect on")
        return msg

    def process(self):

        if not self.config[I2C_ENABLED] or not self.config[DIGITAL_CHANNELS_ENABLED]:
            return

        if not self.voice_out.value and TimeUtils.is_time(self.last_effect_time, self.effect_timeout):
            #self.effect.value = False
            self.voice_out.value = True

            logging.info("activate effect off")
