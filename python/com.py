import serial
import time
import logging

from python.file_watcher import FileWatcher


class Com:
    """A simple example class"""
    i = 12345

    watcher = FileWatcher()

    def get_msg(self):

        if self.watcher.changed():
            return self.watcher.get_last_key()

        print('Running. Press CTRL-C to exit.')
        with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
            time.sleep(0.1)  # wait for serial to open
            if arduino.isOpen():
                print("{} connected!".format(arduino.port))
                try:
                    while True:
                        cmd = input("Enter command : ")
                        arduino.write(cmd.encode())
                        # time.sleep(0.1) #wait for arduino to answer
                        while arduino.inWaiting() == 0:
                            pass
                        if arduino.inWaiting() > 0:
                            answer = arduino.readline()
                            print(answer)
                            arduino.flushInput()  # remove data after reading
                            logging.info('received from arduino'+answer)
                except KeyboardInterrupt:
                    print("KeyboardInterrupt has been caught.")
