import logging
import random

from adafruit_servokit import ServoKit

from dadou_utils_ros.misc import Misc
from dadou_utils_ros.utils.time_utils import TimeUtils
from dadou_utils_ros.utils_static import NORMAL, RANDOM, RANDOM_MOVE_MAX, RANDOM_MOVE_MIN, RANDOM_TIME_MAX, \
    RANDOM_TIME_MIN, \
    RANDOM_DURATION, MODE, ANIMATION, UP, DOWN, STOP

INPUT_MIN = 0
INPUT_MAX = 99

SERVO_MIN = 0
STEP = 5


class Servo:
    random_time_min = 0
    random_time_max = 0
    random_move_min = 0
    random_move_max = 0
    random_last_time = 0
    random_next_time = 0
    random_start_time = 0
    random_duration = 0

    def __init__(self, type, pwm_channel_nb, default_pos, servo_max, i2c_enabled, pwm_channels_enabled):

        self.enabled = (i2c_enabled or pwm_channels_enabled) and Misc.is_raspberrypi()
        logging.info("init  {} servo i2c enabled {}".format(type, Misc.is_raspberrypi()))

        if not self.enabled:
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

        logging.info("{} servo update with {}".format(self.type, msg))

        if not self.enabled:
            return msg

        if msg[self.type] == STOP:
            logging.info("update {} servo with default pos {}".format(self.type, self.default_pos))
            self.set_angle(self.default_pos)
            self.mode = NORMAL

        if msg and self.type in msg:
            if msg[self.type] == UP:
                if self.pwm_channel.angle < self.servo_max - STEP:
                    self.pwm_channel.angle = self.pwm_channel.angle + STEP
            if msg[self.type] == DOWN:
                if self.pwm_channel.angle > STEP:
                    self.pwm_channel.angle = self.pwm_channel.angle - STEP

        if msg and self.type in msg:
            if isinstance(msg[self.type], float) or isinstance(msg[self.type], int):
                if 0 < msg[self.type] <= 1:
                    value = msg[self.type] * 100
                else:
                    value = msg[self.type]
                self.set_angle(value)
                self.mode = NORMAL
            else:
                if isinstance(msg[self.type], dict) and MODE in msg[self.type]:
                    #let the last instruction finish
                    if self.mode == RANDOM:
                        return
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

        return msg

    def set_angle(self, value):
        if value > 0 and value <= 1:
            value = value * 100
        target_pos = Misc.mapping(value, INPUT_MIN, INPUT_MAX, SERVO_MIN, self.servo_max)
        logging.debug("update servo {} with value {} for target {}".format(self.type, value, target_pos))
        self.pwm_channel.angle = target_pos

    def process(self):
        if self.enabled and self.mode == RANDOM:
            if self.random_start_time != 0 and TimeUtils.is_time(self.random_start_time, self.random_duration):
                self.mode = NORMAL
            if TimeUtils.is_time(self.random_last_time, self.random_next_time):
                value = random.randint(self.random_move_min, self.random_move_max)
                self.set_angle(value)
                self.random_last_time = TimeUtils.current_milli_time()
                self.random_next_time = random.randint(self.random_time_min, self.random_time_max)
