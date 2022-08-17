import logging

from dadou_utils.com.serial_device import SerialDevice
from dadou_utils.misc import Misc
from dadou_utils.time.time_utils import TimeUtils

from dadourobot.robot_factory import RobotFactory


class Head:

    timeout = 200
    last_time = TimeUtils.current_milli_time()

    def __init__(self):
        mega_id = RobotFactory().config.HEAD_MEGA_ID
        self.mega = SerialDevice(mega_id, 7)
        self.last_msg = None

    def process(self, msg):
        if TimeUtils.is_time(self.last_time, self.timeout) and msg and hasattr(msg, 'neck') and msg.neck and msg.neck != self.last_msg:
            logging.info("neck instruction {}".format(str(msg.neck)))

            self.mega.send_msg(msg.neck, True)
            self.last_time = TimeUtils.current_milli_time()
            self.last_msg = msg.neck

        else:
            logging.debug("no neck instruction ")
            #self.mega.get_msg()
        #if msg and hasattr(msg, 'key'):
        #    logging.info("neck instruction {}".format(ord(msg.key)))
        #    self.mega.send_msg(msg.key, True)
