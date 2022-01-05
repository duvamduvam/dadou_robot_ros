import serial
import time
import logging

from python.file_watcher import FileWatcher


class Com:
    arduino_enable = True
    arduino = serial.Serial("/dev/serial1", 115200, timeout=1)
    #arduino = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
    # time.sleep(0.1)  # wait for serial to open
    watcher = FileWatcher()

    def get_msg(self):
        if self.watcher.changed():
            return self.watcher.get_last_key()

        if self.arduino_enable & self.arduino.isOpen():
            logging.info("{} connected!".format(self.arduino.port))
            if self.arduino.inWaiting() > 0:
                msg = self.arduino.readline().decode('utf-8').rstrip()
                self.arduino.flushInput()  # remove data after reading
                logging.info('received from arduino' + msg)
                return msg
        return None

    def send_msg(self, msg):
        if self.arduino.isOpen():
            self.arduino.write(msg)
