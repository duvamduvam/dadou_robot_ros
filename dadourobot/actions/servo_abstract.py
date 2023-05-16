import logging

from adafruit_servokit import ServoKit
from dadou_utils.misc import Misc
from dadourobot.input.global_receiver import GlobalReceiver

INPUT_MIN = 0
INPUT_MAX = 99

SERVO_MIN = 0


class ServoAbstract:

    def __init__(self, type, pwm_channel_nb, default_pos, servo_max, i2c_enabled, pwm_channels_enabled, receiver):

        logging.info("init  {} servo".format(type))
        self.receiver = receiver
        self.enabled = i2c_enabled or pwm_channels_enabled
        if not self.enabled:
            logging.warning("i2c pwm disabled")
            return

        try:
            self.self_pwm_channels = ServoKit(channels=16)
            self.pwm_channel = self.self_pwm_channels.servo[pwm_channel_nb]

        except ValueError as err:
            logging.error("{} : can't connect to i2c".format(type))
            self.enabled = False
            return

        self.type = type
        self.servo_max = servo_max
        self.update({self.type: default_pos})

    def update(self, msg):

        if not self.enabled:
            return msg

        if msg and self.type in msg:
            value = Misc.cast_float(msg[self.type])
            if value > 0 and value <= 1:
                value = value * 100
            target_pos = Misc.mapping(value, INPUT_MIN, INPUT_MAX, SERVO_MIN, self.servo_max)
            logging.info("update servo {} with key {} for target {}".format(self.type, value, target_pos))
            self.pwm_channel.angle = target_pos

            del msg[self.type]
            self.receiver.write_msg(msg)

        return msg

    def process(self):
        pass