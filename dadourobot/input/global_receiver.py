import asyncio
import copy
import fcntl
import logging
import json
import multiprocessing
import os
import threading
import time
from json import JSONDecodeError
from watchdog.events import LoggingEventHandler

from dadou_utils.static_value import StaticValue
from dadou_utils.com.input_messages_list import InputMessagesList
#from dadou_utils.com.lora_radio import LoraRadio
#from dadou_utils.com.serial_device import SerialDevice
from dadou_utils.com.lora_radio import LoraRadio
from dadou_utils.com.ws_server import WsServer
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import INPUT_MESSAGE_FILE, KEY, TIME, RANDOM, MAIN_THREAD, NEW_DATA, TYPES, MULTI_THREAD
from watchdog.observers import Observer

from dadourobot.input.file_watcher import FileWatcher
from dadourobot.sequences.random_animation_start import RandomAnimationStart


class GlobalReceiver:

    prefix = '<'
    postfix = '>'
    messages = InputMessagesList()

    def __init__(self, config, animation_manager=None):
        #self.mega_lora_radio = SerialDevice('modem', self.config.RADIO_MEGA_ID, 7)
        #self.mega_lora_radio = device_manager.get_device(RobotStatic.RADIO_MEGA)
        #glove_id = SerialDevice.USB_ID_PATH + "usb-Raspberry_Pi_Pico_E6611CB6976B8D28-if00"
        #self.glove = SerialDevice(glove_id)
        self.config = config
        if TYPES in config:
            self.types = config[TYPES]
        self.main_thread = MAIN_THREAD in config and config[MAIN_THREAD]

        if self.main_thread:
            WsServer().start()
        #self.lora_radio = LoraRadio(self.config)
        self.last_msg_time = 0
        self.animation_manager = animation_manager

        if config[MULTI_THREAD]:
            self.file_watcher = FileWatcher()
            observer = Observer()
            observer.schedule(self.file_watcher, path=INPUT_MESSAGE_FILE, recursive=False)
            observer.start()

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
            if self.animation_manager:
                self.animation_manager.update(msg)

        if self.animation_manager and not self.animation_manager.playing and self.config[RANDOM]:
            self.animation_manager.random()
            #return self.write_msg(self.animation_manager.event())

        if self.animation_manager:
            msg.update(self.animation_manager.event())

        if msg and len(msg) > 0:
            logging.info('received animation'.format(msg))
            return msg

        #radio_msg = self.lora_radio.receive_msg()
        #if radio_msg:
        #    logging.info('received lora msg : {}'.format(radio_msg))
        #    return radio_msg

    def multi_get(self):
        if self.main_thread:
            msg = self.get_msg()
            if msg:
                self.write_msg_plus_time(msg)
                return msg
        else:
            return self.read_msg()

    @staticmethod
    def write_msg(msg):
        asyncio.run(GlobalReceiver.write_msg_async(msg))

    @staticmethod
    async def write_msg_async(msg):
        if msg:
            json_object = json.dumps(msg, indent=4)
            with multiprocessing.Lock():
                with open(INPUT_MESSAGE_FILE, "w") as j:
                    j.write(json_object)

            logging.info("new msg written {}".format(msg))

    def write_msg_plus_time(self, msg):
        t = TimeUtils.current_milli_time()
        time_msg = copy.copy(msg)
        for key in msg.keys():
            if not isinstance(msg[key], list):
            #if len(msg[key]):
                time_msg[key] = [t, msg[key]]
            else:
                time_msg[key] = msg[key]

        self.write_msg(time_msg)

    def write_values(self, values):
        msg = copy.copy(self.file_watcher.last_msg)
        msg.update(values)
        self.write_msg(msg)

    def read_msg(self):
        if StaticValue.get(NEW_DATA):
            StaticValue.set(NEW_DATA, False)
            with multiprocessing.Lock():
                msg = self.file_watcher.get_msg()
            return msg


        """if not self.last_msg_time == os.stat(INPUT_MESSAGE_FILE).st_mtime:
            self.last_msg_time = os.stat(INPUT_MESSAGE_FILE).st_mtime
            with open(INPUT_MESSAGE_FILE, 'r') as j:
                try:
                   return json.loads(j.read())
                except JSONDecodeError:
                    logging.debug("{} wrong format {}".format(INPUT_MESSAGE_FILE, j))"""



    def return_msg(self, msg, log_text):
        if msg:
            logging.info(log_text.format(msg))
            return msg
    #def filter_msg(self, m):
    #    return self.msg.set(m)


