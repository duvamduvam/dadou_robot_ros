import logging

import board
import pwmio
from digitalio import DigitalInOut

from python.config import Config
from python.utils import Utils


class Wheel:
    left = 0
    right = 0

    # TODO check steps
    pwm_step = 50
    time_step = 50
    move_time = 0
    move_timeout = 500

    utils = Utils()

    def __init__(self, config:Config):
        self.left_pwm = pwmio.PWMOut(config.LEFT_PWM_PIN, frequency=5000, duty_cycle=0)
        self.right_pwm = pwmio.PWMOut(config.RIGHT_PWM_PIN, frequency=5000, duty_cycle=0)
        self.dir_left = DigitalInOut(config.LEFT_DIR_PIN)
        self.dir_right = DigitalInOut(config.RIGHT_DIR_PIN)

    def update(self, key: str):
        if key:
            logging.debug("update wheel with key : " + key)
            left = self.utils.translate(ord(key[0]))
            right = self.utils.translate(ord(key[1]))
            self.dir_left = self.utils.is_positive(left)
            self.dir_right = self.utils.is_positive(right)
            self.move_time = Utils.current_milli_time()
        else:
            if Utils.is_time(self.move_time, self.move_timeout):
                self.stop()

    def stop(self):
        self.left_pwm.duty_cycle = 0
        self.right_pwm.duty_cycle = 0

    def process(self):
        # logging.debug("process wheel")
        if (self.left_pwm.duty_cycle != self.left and self.right_pwm.duty_cycle != self.right) \
                and Utils.current_milli_time() - self.move_time > self.time_step:
            self.update_pwm(self.left, self.left_pwm.duty_cycle)
            self.update_pwm(self.right, self.right_pwm.duty_cycle)

    def update_pwm(self, target, pwm: pwmio.PWMOut):
        if pwm.duty_cycle < target:
            if (target - pwm.duty_cycle) < self.pwm_step:
                pwm.duty_cycle = target
            else:
                pwm.duty_cycle += self.pwm_step
        else:
            if (pwm.duty_cycle - target) < self.pwm_step:
                pwm.duty_cycle = target
            else:
                pwm.duty_cycle -= self.pwm_step
