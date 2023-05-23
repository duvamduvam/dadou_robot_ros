import logging
import random

from adafruit_servokit import ServoKit
from dadou_utils.misc import Misc
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import NORMAL, RANDOM, RANDOM_MOVE_MAX, RANDOM_MOVE_MIN, RANDOM_TIME_MAX, RANDOM_TIME_MIN, \
    RANDOM_DURATION, MODE, ANIMATION, STOP
from dadourobot.input.global_receiver import GlobalReceiver

INPUT_MIN = 0
INPUT_MAX = 99

SERVO_MIN = 0


class Servo:
    random_time_min = 0
    random_time_max = 0
    random_move_min = 0
    random_move_max = 0
    random_last_time = 0
    random_next_time = 0
    random_start_time = 0
    random_duration = 0

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
        self.mode = NORMAL
        self.servo_max = servo_max
        self.default_pos = default_pos
        self.set_angle(default_pos)

    def update(self, msg):

        if not self.enabled:
            return msg

        if ANIMATION in msg and not msg[ANIMATION]:
            logging.info("update {} servo with default pos {}".format(self.type, self.default_pos))
            self.set_angle(self.default_pos)
            self.mode = NORMAL

        if msg and self.type in msg:
            if isinstance(msg[self.type], float) or isinstance(msg[self.type], int) or Misc.cast_int(msg[self.type]):
                value = Misc.cast_int(msg[self.type])
                self.set_angle(value)
            else:
                if isinstance(msg[self.type], dict) and MODE in msg[self.type]:
                    self.mode = msg[self.type][MODE]
                    if self.mode == RANDOM:
                        if RANDOM_MOVE_MAX in msg[self.type] and RANDOM_MOVE_MIN in msg[self.type]\
                                and RANDOM_TIME_MAX in msg[self.type] and RANDOM_TIME_MIN in msg[self.type]:
                            self.random_time_min = msg[self.type][RANDOM_TIME_MIN]
                            self.random_time_max = msg[self.type][RANDOM_TIME_MAX]
                            self.random_move_min = msg[self.type][RANDOM_MOVE_MIN]
                            self.random_move_max = msg[self.type][RANDOM_MOVE_MAX]
                            if RANDOM_DURATION in msg:
                                self.random_duration = msg[self.type][RANDOM_DURATION]
                                self.random_start_time = TimeUtils.current_milli_time()
                            self.random_last_time = TimeUtils.current_milli_time()
                            self.random_next_time = random.randint(self.random_time_min, self.random_time_max)
                        else:
                            logging.error("missing parameter in random instruction {}".format(msg[self.type]))
                            self.mode = RANDOM
            del msg[self.type]
            self.receiver.write_msg(msg)

        return msg

    def set_angle(self, value):
        if value > 0 and value <= 1:
            value = value * 100
        target_pos = Misc.mapping(value, INPUT_MIN, INPUT_MAX, SERVO_MIN, self.servo_max)
        logging.info("update servo {} with value {} for target {}".format(self.type, value, target_pos))
        self.pwm_channel.angle = target_pos

    def process(self):
        if self.mode == RANDOM:
            if self.random_start_time != 0 and TimeUtils.is_time(self.random_start_time, self.random_duration):
                self.mode = NORMAL
            if TimeUtils.is_time(self.random_last_time, self.random_next_time):
                value = random.randint(self.random_move_min, self.random_move_max)
                self.set_angle(value)
                self.random_last_time = TimeUtils.current_milli_time()
                self.random_next_time = random.randint(self.random_time_min, self.random_time_max)
