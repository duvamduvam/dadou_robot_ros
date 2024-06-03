import logging
import random

from adafruit_servokit import ServoKit

from dadou_utils_ros.misc import Misc
from dadou_utils_ros.utils.time_utils import TimeUtils
from dadou_utils_ros.utils_static import NORMAL, RANDOM, RANDOM_MOVE_MAX, RANDOM_MOVE_MIN, RANDOM_TIME_MAX, \
    RANDOM_TIME_MIN, \
    RANDOM_DURATION, MODE, ANIMATION, UP, DOWN, STOP, DEFAULT

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

    def __init__(self, servo_type, pwm_channel_nb, default_pos, servo_max, i2c_enabled, pwm_channels_enabled):

        self.enabled = (i2c_enabled or pwm_channels_enabled) and Misc.is_raspberrypi()
        logging.info("init  {} servo i2c enabled {}".format(servo_type, Misc.is_raspberrypi()))

        if not self.enabled:
            return

        try:
            self.self_pwm_channels = ServoKit(channels=16)
            self.pwm_channel = self.self_pwm_channels.servo[pwm_channel_nb]

        except ValueError as err:
            logging.error("{} : can't connect to i2c".format(servo_type))
            self.enabled = False
            return

        self.servo_type = servo_type
        self.mode = NORMAL
        self.servo_max = servo_max
        self.default_pos = default_pos
        self.set_angle(default_pos)

    def update(self, msg):

        if not self.enabled:
            return msg

        logging.info("{} servo update with {}".format(self.servo_type, msg))

        if msg[self.servo_type] == STOP:
            logging.info("update {} servo with default pos {}".format(self.servo_type, self.default_pos))
            self.set_angle(self.default_pos)
            self.mode = NORMAL

        #parameter default angle
        if msg and self.servo_type in msg and isinstance(msg[self.servo_type], dict) and DEFAULT in msg[self.servo_type]:
            default_angle = float(msg[self.servo_type][DEFAULT])
            logging.info("{} servo default {}".format(self.servo_type, default_angle))
            self.default_pos = default_angle
            self.set_angle(default_angle)

        if msg and self.servo_type in msg:
            if msg[self.servo_type] == UP:
                if self.pwm_channel.angle < self.servo_max - STEP:
                    self.pwm_channel.angle = self.pwm_channel.angle + STEP
            elif msg[self.servo_type] == DOWN:
                if self.pwm_channel.angle > STEP:
                    self.pwm_channel.angle = self.pwm_channel.angle - STEP
            elif isinstance(msg[self.servo_type], float):
                if 0 <= msg[self.servo_type] <= 1:
                    value = msg[self.servo_type] * 100
                else:
                    value = msg[self.servo_type]
                self.set_angle(value)
                self.mode = NORMAL
            else:
                if isinstance(msg[self.servo_type], dict) and MODE in msg[self.servo_type]:
                    #let the last instruction finish
                    if self.mode == RANDOM:
                        return
                    self.mode = msg[self.servo_type][MODE]
                    if self.mode == RANDOM:
                        if RANDOM_MOVE_MAX in msg[self.servo_type] and RANDOM_MOVE_MIN in msg[self.servo_type]\
                                and RANDOM_TIME_MAX in msg[self.servo_type] and RANDOM_TIME_MIN in msg[self.servo_type]:
                            self.random_time_min = msg[self.servo_type][RANDOM_TIME_MIN]
                            self.random_time_max = msg[self.servo_type][RANDOM_TIME_MAX]
                            self.random_move_min = msg[self.servo_type][RANDOM_MOVE_MIN]
                            self.random_move_max = msg[self.servo_type][RANDOM_MOVE_MAX]
                            if RANDOM_DURATION in msg:
                                self.random_duration = msg[self.servo_type][RANDOM_DURATION]
                                self.random_start_time = TimeUtils.current_milli_time()
                            self.random_last_time = TimeUtils.current_milli_time()
                            self.random_next_time = random.randint(self.random_time_min, self.random_time_max)
                        else:
                            logging.error("missing parameter in random instruction {}".format(msg[self.servo_type]))
                            self.mode = RANDOM

        return msg

    def set_angle(self, value):
        if value > 0 and value <= 1:
            value = value * 100
        target_pos = Misc.mapping(value, INPUT_MIN, INPUT_MAX, SERVO_MIN, self.servo_max)
        logging.debug("update servo {} with value {} for target {}".format(self.servo_type, value, target_pos))
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
