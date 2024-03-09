import logging
from builtins import staticmethod

import serial
from input.file_watcher import FileWatcher
from input.message import Message


class Com:
    arduino_enable = True
    #arduino = serial.Serial("/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Due_Prog._Port_85036313230351C0A132-if00", 115200, timeout=1)
    arduino = serial.Serial("/dev/serial0", 115200, timeout=1)
    #arduino = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)
    # arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
    # time.sleep(0.1)  # wait for serial to open
    watcher = FileWatcher()
    INPUT_SIZE = 7

    def get_msg(self) -> Message:
        if self.watcher.changed():
            return self.watcher.get_last_key()

        if self.arduino_enable & self.arduino.isOpen():
            # logging.info("{} connected!".format(self.arduino.port))
            if self.arduino.inWaiting() > 0:
                msg = self.arduino.read(self.INPUT_SIZE).decode('utf-8').rstrip()
                self.arduino.flushInput()  # remove data after reading
                logging.info('received from arduino' + msg)
                return self.decode(msg)
        return None

    def send_msg(self, msg):
        if self.arduino.isOpen():
            self.arduino.write(msg)

    @staticmethod
    def decode(msg: str):
        if msg.startswith(Message.PREFIX) and msg.endswith(Message.POSTFIX):
            return Message(msg[1], msg[2], msg[3], msg[4] + msg[5])
        else:
            logging.error("wrong message : \"" + msg + "\"")
            return None
