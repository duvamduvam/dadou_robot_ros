import logging

import adafruit_pca9685
import board
import busio
import pwmio

from dadou_utils.misc import Misc
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import ANGLO, WHEEL_RIGHT, WHEEL_LEFT, JOY, WHEELS, KEY, \
    CMD_FORWARD, CMD_BACKWARD, CMD_LEFT, CMD_RIGHT, I2C_ENABLED, PWM_CHANNELS_ENABLED, \
    WHEEL_LEFT_PWM, WHEEL_RIGHT_PWM, WHEEL_LEFT_DIR, WHEEL_RIGHT_DIR, STRAIGHT
from dadourobot.input.global_receiver import GlobalReceiver
from dadourobot.move.anglo_meter_translator import AngloMeterTranslator


class Wheel:
    left = 0
    right = 0
    mode = None

    # TODO check steps
    PWM_STEP = 5
    TIME_STEP = 50
    move_time = 0
    MOVE_TIMEOUT = 400
    MIN_PWM = 5000
    MAX_PWM = 30000
    MAX_DIR = 65530
    FREQUENCY = 500

    starting_angle_x = 0
    target_pos_x = 0
    half_turn = False
    front_pos = 0

    front_pos_margin = 3
    angle_margin = 5

    sensor = None

    animation_ongoing = False

    test_speed = 0
    test_direction = 0
    last_move = 0

    def __init__(self, config):
        self.config = config
        self.enabled = self.config[I2C_ENABLED] or self.config[PWM_CHANNELS_ENABLED]
        if not self.enabled:
            logging.warning("i2c pwm disabled")
            return

        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            pca9685 = adafruit_pca9685.PCA9685(i2c)
            pca9685.frequency = 60
        except ValueError as err:
            logging.error("can't connect to to i2c")
            self.enabled = False
            return

        #self.left_pwm = pwmio.PWMOut(Pin(config.LEFT_PWM_PIN))
        #self.right_pwm = pwmio.PWMOut(Pin(config.RIGHT_PWM_PIN))
        #self.dir_left = digitalio.DigitalInOut(Pin(config.LEFT_DIR_PIN))
        #self.dir_left.direction = digitalio.Direction.OUTPUT
        #self.dir_right = digitalio.DigitalInOut(Pin(config.RIGHT_DIR_PIN))
        #self.dir_right.direction = digitalio.Direction.OUTPUT

        #i2c = busio.I2C(board.SCL, board.SDA)
        #pca9685 = adafruit_pca9685.PCA9685(i2c)
        #pca9685.frequency = 60

        self.left_pwm = pca9685.channels[self.config[WHEEL_LEFT_PWM]]
        self.right_pwm = pca9685.channels[self.config[WHEEL_RIGHT_PWM]]
        self.dir_left = pca9685.channels[self.config[WHEEL_LEFT_DIR]]
        self.dir_right = pca9685.channels[self.config[WHEEL_RIGHT_DIR]]

        #self.dir_left = pwmio.PWMOut(board.D6)
        #self.dir_right = pwmio.PWMOut(board.D5)
        #self.dir_left = pwmio.PWMOut(Pin(config.LEFT_DIR_PIN))
        #self.dir_right = pwmio.PWMOut(Pin(config.RIGHT_DIR_PIN))
        #self.due = None

        self.anglo_meter_translator = AngloMeterTranslator()

    def set_9dof(self, sensor):
        self.sensor = sensor

    def update(self, msg):

        #if msg and ANIMATION in msg and WHEEL_LEFT in msg and WHEEL_RIGHT in msg:
        #    self.animation_ongoing = msg[ANIMATION]

        if not self.enabled:
            return msg

        if not msg:
            return msg

        if KEY in msg and (msg[KEY] == self.config[CMD_FORWARD] or msg[KEY] == self.config[CMD_BACKWARD] or msg[KEY] == self.config[CMD_LEFT] or msg[KEY] == self.config[CMD_RIGHT]):
            if msg[KEY] == self.config[CMD_FORWARD]:
                self.update_cmd(30, 30)
            elif msg[KEY] == self.config[CMD_BACKWARD]:
                self.update_cmd(-30, -30)
            elif msg[KEY] == self.config[CMD_LEFT]:
                self.update_cmd(-30, 30)
            elif msg[KEY] == self.config[CMD_RIGHT]:
                self.update_cmd(30, -30)

        if ANGLO in msg:
            wheels = self.anglo_meter_translator.translate(msg[ANGLO])
            self.update_cmd(wheels[0], wheels[1])
            del msg[ANGLO]
        if JOY in msg:
            wheels = self.anglo_meter_translator.translate(msg[JOY])
            self.update_cmd(wheels[0], wheels[1])
            del msg[JOY]
        if WHEEL_LEFT in msg and WHEEL_RIGHT in msg:
            self.update_cmd(msg[WHEEL_LEFT], msg[WHEEL_RIGHT])
            del msg[WHEEL_LEFT]
            del msg[WHEEL_RIGHT]
        if WHEELS in msg:
            self.update_cmd(int(msg[WHEELS][0]*100), int(msg[WHEELS][1]*100))
            del msg[WHEELS]

        if ANGLO in msg or JOY in msg or WHEEL_LEFT in msg or WHEEL_RIGHT in msg or WHEELS in msg:
            GlobalReceiver.write_msg(msg)
        return msg

    def update_cmd(self, left_wheel, right_wheel):
        self.left = left_wheel
        self.right = right_wheel

        logging.info("update wheel with left : " + str(left_wheel) + " right : " + str(right_wheel))

        self.left_pwm.duty_cycle = Misc.mapping(abs(left_wheel), 0, 100, self.MIN_PWM, self.MAX_PWM)
        self.right_pwm.duty_cycle = Misc.mapping(abs(right_wheel), 0, 100, self.MIN_PWM, self.MAX_PWM)

        self.set_direction(left_wheel, self.dir_left)
        self.set_direction(right_wheel, self.dir_right)

        self.move_time = TimeUtils.current_milli_time()
        logging.info("cmd left {} duty cycle {} direction {} // cmd right {} duty cycle {} direction {}".
                        format(left_wheel, self.left_pwm.duty_cycle, self.dir_left.duty_cycle, right_wheel, self.right_pwm.duty_cycle, self.dir_right.duty_cycle))


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
        logging.info("wheels stopped")

    def check_stop(self):

        if not self.enabled:
            return

        if not self.animation_ongoing and TimeUtils.is_time(last_time=self.move_time, time_out=self.MOVE_TIMEOUT):
            self.stop()

    def process(self):

        if not self.enabled:
            return

        if self.mode == STRAIGHT:
            self.move_straight()

        self.check_stop()

    def move_straight(self):
        if self.starting_angle_x != -1 and self.sensor:
            if self.starting_angle_x > self.sensor.euler[0]:
                self.update_cmd(self.left+1, self.right-1)
            else:
                self.update_cmd(self.left-1, self.right+1)

    def start_circle(self, left, right):
        if self.sensor:
            self.half_turn = False
            self.starting_angle_x = self.sensor.euler[0]
            self.update_cmd(left, right)
        else:
            logging.error("9dof not set")

    def move_circle(self):
        if self.starting_angle_x != -1 and self.sensor:
            if self.half_turn and abs(self.starting_angle_x - self.sensor.euler[0]) <= self.angle_margin:
                return True
            if not self.half_turn and abs(self.starting_angle_x - self.sensor.euler[0])> 180:
                self.half_turn = True
        return False


    def set_front_pos(self):
        if self.sensor:
            self.front_pos = self.sensor.euler[0]
        else:
            logging.error("9dof not set")

    def get_back_front(self):
        if self.sensor:
            if abs(self.sensor.euler[0] - self.front_pos) < self.front_pos_margin:
                logging.info("front position reached")
            else:
                if self.sensor.euler[0] - self.front_pos:
                    self.update_cmd(self.left - 1, self.right + 1)

        else:
            logging.error("9dof not set")
        return False

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
