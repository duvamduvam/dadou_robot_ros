import logging

from move.anglo_meter_translator import AngloMeterTranslator
from robot_config import MAIN_DUE

from dadou_utils.com.serial_devices_manager import SerialDeviceManager
from dadou_utils.utils_static import KEY, ANGLO


class MainDueCom:

    def __init__(self, device_manager:SerialDeviceManager):
        self.main_due = device_manager.get_device(MAIN_DUE)
        if not self.main_due:
            logging.error("main due not connected")
        self.anglo_meter_translator = AngloMeterTranslator()

    def send_dict(self, msg:dict):
        if KEY in msg and msg[KEY] not in "m":
            self.send("  "+msg[KEY])
        if ANGLO in msg:
            move = self.get_wheel_instruction(msg[ANGLO])
            self.send(move+"   ")

    def send(self, msg:str):
        if msg:
            msg = "<{}>".format(msg)
            self.main_due.send_msg(msg, True)
            logging.info("send {} to due".format(msg))
        else:
            logging.warn("message empty")

    def get_wheel_instruction(self, command):
        wheels = self.anglo_meter_translator.translate(command)
        msg = [chr(wheels[0]), chr(wheels[1])]
        return ''.join(msg)

    def get_msg(self):
        self.main_due.get_msg(0)