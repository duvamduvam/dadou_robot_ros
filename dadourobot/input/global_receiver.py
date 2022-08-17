import logging

from dadou_utils.com.serial_device import SerialDevice
from dadou_utils.com.ws_server import WsServer
from dadou_utils.misc import Misc

from dadourobot.input.message import Message
from dadourobot.robot_factory import RobotFactory
from dadourobot.robot_static import RobotStatic


class GlobalReceiver:

    prefix = '<'
    postfix = '>'
    msg = Message()

    def __init__(self):
        self.config = RobotFactory().config
        self.lora_radio = SerialDevice(self.config.RADIO_MEGA_ID, 7)
        #glove_id = SerialDevice.USB_ID_PATH + "usb-Raspberry_Pi_Pico_E6611CB6976B8D28-if00"
        #self.glove = SerialDevice(glove_id)
        WsServer().start()
        self.ws_messages = RobotFactory().ws_message

    def get_msg(self):
        radio_msg = self.lora_radio.get_msg()
        if radio_msg:
            logging.info('received radio msg : {}'.format(radio_msg))
            return self.filter_msg(radio_msg)
        """glove = self.glove.get_msg()
        if glove:
            logging.info('received glove msg : {}'.format(glove))
            return glove"""
        ws_msg = self.ws_messages.get_msg()
        if ws_msg:
            logging.info('received ws msg : {}'.format(ws_msg))
            return ws_msg

    def filter_msg(self, m):
        return self.msg.set(m)


