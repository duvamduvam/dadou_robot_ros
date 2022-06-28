import logging

from dadou_utils.com.serial_device import SerialDevice

from dadourobot.robot_factory import RobotFactory


class Head:

    def __init__(self):
        mega_id = RobotFactory().config.HEAD_MEGA_ID
        self.mega = SerialDevice(mega_id)

    def process(self, msg):
        if msg and hasattr(msg, 'neck'):
            #logging.info("neck instruction {}".format(ord(msg.neck)))
            self.mega.send_msg(msg.neck, True)
            #self.mega.get_msg()
        if msg and hasattr(msg, 'key'):
            self.mega.send_msg(msg.key, True)
