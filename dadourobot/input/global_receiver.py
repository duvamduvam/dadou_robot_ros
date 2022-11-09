import logging

from dadou_utils.com.input_messages_list import InputMessagesList
from dadou_utils.com.lora_radio import LoraRadio
from dadou_utils.com.serial_device import SerialDevice
from dadou_utils.com.ws_server import WsServer
from dadou_utils.misc import Misc

from dadourobot.input.message import Message
from dadourobot.robot_factory import RobotFactory


class GlobalReceiver:

    prefix = '<'
    postfix = '>'
    messages = InputMessagesList()

    def __init__(self, device_manager):
        self.config = RobotFactory().config
        #self.mega_lora_radio = SerialDevice('modem', self.config.RADIO_MEGA_ID, 7)
        #self.mega_lora_radio = device_manager.get_device(RobotStatic.RADIO_MEGA)
        #glove_id = SerialDevice.USB_ID_PATH + "usb-Raspberry_Pi_Pico_E6611CB6976B8D28-if00"
        #self.glove = SerialDevice(glove_id)
        WsServer().start()
        self.lora_radio = LoraRadio(self.config)

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
            logging.info('received ws msg : {}'.format(msg))
            return msg
        radio_msg = self.lora_radio.receive_msg()
        if radio_msg:
            logging.info('received lora msg : {}'.format(radio_msg))
            return radio_msg


    #def filter_msg(self, m):
    #    return self.msg.set(m)


