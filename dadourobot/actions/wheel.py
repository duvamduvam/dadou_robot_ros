import logging

import digitalio
import pwmio
from dadou_utils.com.serial_device import SerialDevice
from dadou_utils.misc import Misc
from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import ANGLO, WHEEL_RIGHT, WHEEL_LEFT
from digitalio import DigitalInOut
from microcontroller import Pin

from dadourobot.move.anglo_meter_translator import AngloMeterTranslator


class Wheel:
    left = 0
    right = 0

    # TODO check steps
    pwm_step = 5
    TIME_STEP = 50
    move_time = 0
    MOVE_TIMEOUT = 500
    MAX_PWM = 20000
    MAX_DIR = 65530
    FREQUENCY = 500

    test_speed = 0
    test_direction = 0


    def __init__(self, config):
        self.config = config
        self.left_pwm = pwmio.PWMOut(Pin(config.LEFT_PWM_PIN))
        self.right_pwm = pwmio.PWMOut(Pin(config.RIGHT_PWM_PIN))
        #self.dir_left = digitalio.DigitalInOut(Pin(config.LEFT_DIR_PIN))
        self.dir_left = pwmio.PWMOut(Pin(config.LEFT_DIR_PIN))
        self.dir_right = pwmio.PWMOut(Pin(config.RIGHT_DIR_PIN))
        self.due = None

        self.anglo_meter_translator = AngloMeterTranslator()

    def set_due(self):
        self.due = SerialDevice('head', self.config.MAIN_DUE_ID, 7)

    def send_msg(self, wheels):
        if not self.due:
            self.set_due()
        msg = "W"+str(int(wheels[0]*100))+str(int(wheels[1]*100))
        self.due.send_msg(msg)

    def update(self, msg:dict):
        if ANGLO in msg:
            wheels = self.anglo_meter_translator.translate(msg[ANGLO])
            self.update_cmd(wheels[0], wheels[1])
        if WHEEL_LEFT in msg and WHEEL_RIGHT in msg:
            self.update_cmd(msg[WHEEL_LEFT], msg[WHEEL_RIGHT])

    def update_cmd(self, left_wheel, right_wheel):
        if left_wheel and right_wheel:
            logging.info("update wheel with left : " + str(left_wheel) + " right : " + str(right_wheel))
            #left = self.utils.translate(left_wheel)
            self.left_pwm.duty_cycle = Misc.mapping(abs(left_wheel), 0, 100, 0, self.MAX_PWM)
            #right = self.utils.translate(right_wheel)
            self.right_pwm.duty_cycle = Misc.mapping(abs(right_wheel), 0, 100, 0, self.MAX_PWM)

            self.set_direction(left_wheel, self.dir_left)
            self.set_direction(right_wheel, self.dir_right)
            """if left_wheel >= 0:
                self.dir_left.duty_cycle = self.MAX_DIR
            else:
                self.dir_left.duty_cycle = 0

            if right_wheel >= 0:
                self.dir_right.duty_cycle = self.MAX_DIR
            else:
                self.dir_right.duty_cycle = 0"""

            self.move_time = TimeUtils.current_milli_time()
            logging.info("cmd left {} duty cycle {} direction {} // cmd right {} duty cycle {} direction {}".
                         format(left_wheel, self.left_pwm.duty_cycle, self.dir_left.duty_cycle, right_wheel, self.right_pwm.duty_cycle, self.dir_right.duty_cycle))

        else:
            if TimeUtils.is_time(self.move_time, self.MOVE_TIMEOUT):
                self.stop()

    def set_direction(self, dir, pwm_dir):
        if dir >= 0:
            pwm_dir.duty_cycle = 0
        else:
            pwm_dir.duty_cycle = self.MAX_DIR

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

    def test(self):
        print("speed : {} || direction : {}".format(self.test_speed, self.test_direction))

        self.dir_left.duty_cycle = self.test_direction
        self.dir_right.duty_cycle = self.test_direction

        self.left_pwm.duty_cycle = self.test_speed
        self.right_pwm.duty_cycle = self.test_speed

        self.test_speed += self.pwm_step
        if self.test_speed >= self.MAX_PWM or self.test_speed <= 0:
            if self.test_speed >= self.MAX_PWM:
                self.test_speed = self.MAX_PWM
            else:
                self.test_speed = 0
                if self.test_direction == 0:
                    self.test_direction = self.MAX_DIR
                else:
                    self.test_direction = 0
            self.pwm_step = -self.pwm_step

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
