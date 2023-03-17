import logging

from dadou_utils.utils.time_utils import TimeUtils


class Head:

    timeout = 200
    last_time = TimeUtils.current_milli_time()

    CHAR_MIN = 20
    CHAR_MAX = 150

    def __init__(self, device_manager, config):
        #self.mega = SerialDevice('head', config.HEAD_MEGA_ID, 7)
        self.mega = device_manager.get_device('head')
        self.last_msg = None

    def process(self, msg):
        #TODO improve test attr
        if TimeUtils.is_time(self.last_time, self.timeout) and msg and hasattr(msg, 'neck') \
                and msg.neck and (msg.neck == 'VE' or msg.neck != self.last_msg):
            logging.info("neck instruction {}".format(str(msg.neck)))

            self.mega.send_msg(msg.neck, True)
            self.last_time = TimeUtils.current_milli_time()
            self.last_msg = msg.neck

        else:
            logging.debug("no neck instruction ")

    def send_msg(self, pourcentage):
        head_msg = int(self.CHAR_MIN + ((self.CHAR_MAX - self.CHAR_MIN)*pourcentage))
        logging.info("send to head {}".format(head_msg))
        self.mega.send_msg(chr(head_msg), True)


            #self.mega.get_msg()
        #if msg and hasattr(msg, 'key'):
        #    logging.info("neck instruction {}".format(ord(msg.key)))
        #    self.mega.send_msg(msg.key, True)
