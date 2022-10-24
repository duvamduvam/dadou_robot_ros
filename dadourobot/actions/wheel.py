import logging

import pwmio
from dadou_utils.com.serial_device import SerialDevice
from dadou_utils.time.time_utils import TimeUtils
from digitalio import DigitalInOut
from microcontroller import Pin

from dadourobot.utils import Utils


class Wheel:
    left = 0
    right = 0

    # TODO check steps
    pwm_step = 50
    time_step = 50
    move_time = 0
    move_timeout = 500

    utils = Utils()

    def __init__(self, config):
        self.config = config
        self.left_pwm = pwmio.PWMOut(Pin(config.LEFT_PWM_PIN), frequency=500, duty_cycle=0)
        self.right_pwm = pwmio.PWMOut(Pin(config.RIGHT_PWM_PIN), frequency=500, duty_cycle=0)
        self.dir_left = DigitalInOut(Pin(config.LEFT_DIR_PIN))
        self.dir_right = DigitalInOut(Pin(config.RIGHT_DIR_PIN))
        self.due = None

    def set_due(self):
        self.due = SerialDevice('head', self.config.MAIN_DUE_ID, 7)

    def send_msg(self, wheels):
        if not self.due:
            self.set_due()
        msg = "W"+str(int(wheels[0]*100))+str(int(wheels[1]*100))
        self.due.send_msg(msg)

    def update(self, left_wheel, right_wheel):
        if left_wheel and right_wheel:
            logging.info("update wheel with left : " + left_wheel + " right : " + right_wheel)
            left = self.utils.translate(left_wheel)
            right = self.utils.translate(right_wheel)
            self.dir_left = self.utils.is_positive(left)
            self.dir_right = self.utils.is_positive(right)
            self.move_time = TimeUtils.current_milli_time()

            self.dir_left = True
            self.dir_right = True
            self.left_pwm.duty_cycle = 30000
            self.right_pwm.duty_cycle = 60000

        else:
            if TimeUtils.is_time(self.move_time, self.move_timeout):
                self.stop()

    def test(self):
        self.dir_left = False
        self.dir_right = False
        self.left_pwm.duty_cycle = 10000
        self.right_pwm.duty_cycle = 10000

    def stop(self):
        self.left_pwm.duty_cycle = 0
        self.right_pwm.duty_cycle = 0

    def process(self):
        logging.info("process wheels")
        #if (self.left_pwm.duty_cycle != self.left and self.right_pwm.duty_cycle != self.right) \
        #        and Utils.is_time(self.move_time, self.move_timeout):
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

    def send_to_due(self, left, right):
        self.due.send_msg(left+right, True)
