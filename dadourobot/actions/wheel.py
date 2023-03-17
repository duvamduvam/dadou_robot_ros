import logging

import adafruit_pca9685
import board
import busio
import pwmio

from dadou_utils.misc import Misc
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import ANIMATION, ANGLO, WHEEL_RIGHT, WHEEL_LEFT, JOY, WHEELS, KEY

from dadourobot.move.anglo_meter_translator import AngloMeterTranslator
from dadourobot.robot_config import CMD_FORWARD, CMD_BACKWARD, CMD_LEFT, CMD_RIGHT, I2C_ENABLED, PWM_CHANNELS_ENABLED
from dadourobot.robot_config import WHEEL_LEFT_PWM, WHEEL_RIGHT_PWM, WHEEL_LEFT_DIR, WHEEL_RIGHT_DIR


class Wheel:
    left = 0
    right = 0

    # TODO check steps
    PWM_STEP = 5
    TIME_STEP = 50
    move_time = 0
    MOVE_TIMEOUT = 400
    MIN_PWM = 5000
    MAX_PWM = 30000
    MAX_DIR = 65530
    FREQUENCY = 500

    animation_ongoing = False

    test_speed = 0
    test_direction = 0

    def __init__(self):

        if not I2C_ENABLED or not PWM_CHANNELS_ENABLED:
            logging.warning("i2c pwm disabled")
            return

        i2c = busio.I2C(board.SCL, board.SDA)
        pca9685 = adafruit_pca9685.PCA9685(i2c)
        pca9685.frequency = 60

        #self.left_pwm = pwmio.PWMOut(Pin(config.LEFT_PWM_PIN))
        #self.right_pwm = pwmio.PWMOut(Pin(config.RIGHT_PWM_PIN))
        #self.dir_left = digitalio.DigitalInOut(Pin(config.LEFT_DIR_PIN))
        #self.dir_left.direction = digitalio.Direction.OUTPUT
        #self.dir_right = digitalio.DigitalInOut(Pin(config.RIGHT_DIR_PIN))
        #self.dir_right.direction = digitalio.Direction.OUTPUT

        #i2c = busio.I2C(board.SCL, board.SDA)
        #pca9685 = adafruit_pca9685.PCA9685(i2c)
        #pca9685.frequency = 60

        self.left_pwm = pca9685.channels[WHEEL_LEFT_PWM]
        self.right_pwm = pca9685.channels[WHEEL_RIGHT_PWM]
        self.dir_left = pca9685.channels[WHEEL_LEFT_DIR]
        self.dir_right = pca9685.channels[WHEEL_RIGHT_DIR]

        #self.dir_left = pwmio.PWMOut(board.D6)
        #self.dir_right = pwmio.PWMOut(board.D5)
        #self.dir_left = pwmio.PWMOut(Pin(config.LEFT_DIR_PIN))
        #self.dir_right = pwmio.PWMOut(Pin(config.RIGHT_DIR_PIN))
        self.due = None

        self.anglo_meter_translator = AngloMeterTranslator()

    def update(self, msg: dict):

        if not I2C_ENABLED or not PWM_CHANNELS_ENABLED:
            return

        if not msg:
            return

        if KEY in msg and (msg[KEY] == CMD_FORWARD or msg[KEY] == CMD_BACKWARD or msg[KEY] == CMD_LEFT or msg[KEY] == CMD_RIGHT):
            if msg[KEY] == CMD_FORWARD:
                self.update_cmd(30, 30)
            elif msg[KEY] == CMD_BACKWARD:
                self.update_cmd(-30, -30)
            elif msg[KEY] == CMD_LEFT:
                self.update_cmd(-30, 30)
            elif msg[KEY] == CMD_RIGHT:
                self.update_cmd(30, -30)

        if ANGLO in msg:
            wheels = self.anglo_meter_translator.translate(msg[ANGLO])
            self.update_cmd(wheels[0], wheels[1])
        if JOY in msg:
            wheels = self.anglo_meter_translator.translate(msg[JOY])
            self.update_cmd(wheels[0], wheels[1])
        if WHEEL_LEFT in msg and WHEEL_RIGHT in msg:
            self.update_cmd(msg[WHEEL_LEFT], msg[WHEEL_RIGHT])
        if WHEELS in msg:
            self.update_cmd(msg[WHEELS][0]*100, msg[WHEELS][1]*100)

    def update_cmd(self, left_wheel, right_wheel):
        #if left_wheel and right_wheel:
        logging.info("update wheel with left : " + str(left_wheel) + " right : " + str(right_wheel))
            #left = self.utils.translate(left_wheel)
        self.left_pwm.duty_cycle = Misc.mapping(abs(left_wheel), 0, 100, self.MIN_PWM, self.MAX_PWM)
            #right = self.utils.translate(right_wheel)
        self.right_pwm.duty_cycle = Misc.mapping(abs(right_wheel), 0, 100, self.MIN_PWM, self.MAX_PWM)

        self.set_direction(left_wheel, self.dir_left)
        #self.dir_left.value = left_wheel >= 0
        #self.dir_right.value = right_wheel >= 0
            #self.dir_right.value = True
        self.set_direction(right_wheel, self.dir_right)

        self.move_time = TimeUtils.current_milli_time()
        logging.info("cmd left {} duty cycle {} direction {} // cmd right {} duty cycle {} direction {}".
                        format(left_wheel, self.left_pwm.duty_cycle, self.dir_left.duty_cycle, right_wheel, self.right_pwm.duty_cycle, self.dir_right.duty_cycle))

        #else:
        #    if TimeUtils.is_time(self.move_time, self.MOVE_TIMEOUT):
        #        self.stop()

    """def set_direction(self, cmd_dir, pwm_dir):
        value = cmd_dir < 0
        logging.info("cmd dir {} value {}".format(cmd_dir, value))
        pwm_dir.value = value"""

    def set_direction(self, cmd_dir, pwm_dir):
        if cmd_dir >= 0:
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

    def check_stop(self, msg):

        if not I2C_ENABLED or not PWM_CHANNELS_ENABLED:
            return

        if msg and ANIMATION in msg:
            self.animation_ongoing = msg[ANIMATION]

        if not self.animation_ongoing and TimeUtils.is_time(last_time=self.move_time, time_out=self.MOVE_TIMEOUT):
            self.last_update = TimeUtils.current_milli_time()
            self.stop()

    def process(self):

        if not I2C_ENABLED or not PWM_CHANNELS_ENABLED:
            return

        #logging.info("process wheels")
        #if (self.left_pwm.duty_cycle != self.left and self.right_pwm.duty_cycle != self.right) \
        #        and Utils.is_time(self.move_time, self.move_timeout):
        self.update_pwm(self.left, self.left_pwm)
        self.update_pwm(self.right, self.right_pwm)

    def update_pwm(self, target, pwm: pwmio.PWMOut):
        if pwm.duty_cycle < target:
            if (target - pwm.duty_cycle) < self.PWM_STEP:
                pwm.duty_cycle = target
            else:
                pwm.duty_cycle += self.PWM_STEP
        else:
            if (pwm.duty_cycle - target) < self.PWM_STEP:
                pwm.duty_cycle = target
            else:
                pwm.duty_cycle -= self.PWM_STEP

    def send_to_due(self, left, right):
        self.due.send_msg(left+right, True)
