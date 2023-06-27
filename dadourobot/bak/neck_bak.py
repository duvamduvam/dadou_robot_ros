# pip3 install adafruit-circuitpython-servokit
import logging

import pwmio
from adafruit_motor import servo
from microcontroller import Pin
from utils import Utils

from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import NECK


class Neck:

    SERVO_MIN = 0
    SERVO_MAX = 180
    STEP = 10
    DEFAULT_POS = 50
    MARGIN = 5

    target_pos = 0
    current_pos = 0

    last_time = TimeUtils.current_milli_time()
    time_step = 200

    utils = Utils()

    # pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)

    def __init__(self, config):
        self.head_pwm = pwmio.PWMOut(Pin(config.NECK_PIN), frequency=50)
        self.servo = servo.Servo(self.head_pwm)
        self.servo.angle = self.DEFAULT_POS

    #TODO fix move from animation
    def update(self, msg):
        if msg and NECK in msg:
            self.target_pos = msg[NECK] #abs(self.utils.translate(msg))
            logging.debug("update servo key : " + str(msg) + " target :" + str(self.target_pos))
            self.servo.angle = self.target_pos
            self.last_time = TimeUtils.current_milli_time()

    def animate(self):
        if TimeUtils.is_time(self.last_time, self.time_step):
            diff = abs(self.target_pos - self.current_pos)
            # logging.debug("servo target : " + str(self.target_pos) + " current : " + str(self.current_pos) +
            #              " margin : " + str(self.margin))
            if diff > self.MARGIN and self.target_pos != self.current_pos:
                if self.target_pos > self.current_pos:
                    self.next_step(self.STEP)
                else:
                    self.next_step(-self.STEP)

    def next_step(self, step):
        if self.SERVO_MIN <= self.current_pos <= self.SERVO_MAX:
            self.current_pos += step
            logging.info("next_step current position " + str(self.current_pos) + " next step " + str(step))
            self.servo.angle = self.current_pos
        else:
            logging.error("servo step : " + str(step) + " out of range")
