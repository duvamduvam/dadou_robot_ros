import serial
import time
import logging

from python.file_watcher import FileWatcher


class Com:
    """A simple example class"""
    i = 12345

    arduino_enable = False
    arduino = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
    watcher = FileWatcher()

    def get_msg(self):

        if self.watcher.changed():
            return self.watcher.get_last_key()

        time.sleep(0.1)  # wait for serial to open
        if self.arduino_enable & self.arduino.isOpen():
            print("{} connected!".format(self.arduino.port))
            if self.arduino.inWaiting() > 0:
                answer = self.arduino.readline()
                self.arduino.flushInput()  # remove data after reading
                logging.info('received from arduino' + answer)
