import fcntl
import logging
import json
import time
from json import JSONDecodeError

from dadou_utils.com.input_messages_list import InputMessagesList
#from dadou_utils.com.lora_radio import LoraRadio
#from dadou_utils.com.serial_device import SerialDevice
from dadou_utils.com.lora_radio import LoraRadio
from dadou_utils.com.ws_server import WsServer
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import INPUT_MESSAGE_FILE, TIME

from dadourobot.sequences.random_animation_start import RandomAnimationStart



class GlobalReceiver:

    prefix = '<'
    postfix = '>'
    messages = InputMessagesList()

    def __init__(self, animation_manager=None):
        #self.mega_lora_radio = SerialDevice('modem', self.config.RADIO_MEGA_ID, 7)
        #self.mega_lora_radio = device_manager.get_device(RobotStatic.RADIO_MEGA)
        #glove_id = SerialDevice.USB_ID_PATH + "usb-Raspberry_Pi_Pico_E6611CB6976B8D28-if00"
        #self.glove = SerialDevice(glove_id)
        WsServer().start()
        #self.lora_radio = LoraRadio(self.config)

        self.animation_manager = animation_manager

    def get_msg(self):
        #TODO mettre a jour la logique lora pour qu'elle corresponde a la logique dict ws
        #mega_msg = self.mega_lora_radio.get_msg()
        #if mega_msg:
        #    logging.info('received radio msg : {}'.format(mega_msg))
        #    return self.filter_msg(mega_msg)
        """glove = self.glove.get_msg()
        if glove:
            logging.info('received glove msg : {}'.format(glove))
            return glove"""

        msg = self.messages.pop_msg()
        if msg:
            logging.info('received from ws server'.format(msg))
            RandomAnimationStart.value = TimeUtils.current_milli_time()
            if self.animation_manager:
                self.animation_manager.update(msg)
            return self.write_msg(msg)
        if self.animation_manager:
            self.animation_manager.random()
            return self.write_msg(self.animation_manager.event())

        if msg and len(msg) > 0:
            logging.info('received animation'.format(msg))
            return self.write_msg(msg)

        #radio_msg = self.lora_radio.receive_msg()
        #if radio_msg:
        #    logging.info('received lora msg : {}'.format(radio_msg))
        #    return radio_msg

    def write_msg(self, msg):
        msg[TIME] = time.time()
        json_object = json.dumps(msg, indent=4)
        with open(INPUT_MESSAGE_FILE, "w") as j:
            j.write(json_object)
        return msg

    @staticmethod
    def read_msg():
        with open(INPUT_MESSAGE_FILE, 'r') as j:
            try:
                return json.loads(j.read())
            except JSONDecodeError:
                logging.debug("{} wrong format {}".format(INPUT_MESSAGE_FILE, j))

    def return_msg(self, msg, log_text):
        if msg:
            logging.info(log_text.format(msg))
            return msg
    #def filter_msg(self, m):
    #    return self.msg.set(m)


