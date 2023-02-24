# pip3 install adafruit-circuitpython-servokit
import pwmio
import logging
from adafruit_motor import servo
from adafruit_servokit import ServoKit
from dadou_utils.misc import Misc
from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import NECK
from microcontroller import Pin

from dadourobot.utils import Utils


class Neck:

    INPUT_MIN = 0
    INPUT_MAX = 99

    SERVO_MIN = 0
    SERVO_MAX = 180
    STEP = 10
    DEFAULT_POS = 110
    MARGIN = 5

    SERVO_POS = 0

    target_pos = 0
    current_pos = 0

    last_time = TimeUtils.current_milli_time()
    time_step = 200

    utils = Utils()

    # pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)

    def __init__(self, config):
        self.self_pwm_channels = ServoKit(channels=16)
        self.self_pwm_channels.servo[self.SERVO_POS].angle = self.DEFAULT_POS

    #TODO fix move from animation
    def update(self, msg):
        if msg and NECK in msg:
            self.target_pos = Misc.mapping(int(msg[NECK]),self.INPUT_MIN, self.INPUT_MAX, self.SERVO_MIN, self.SERVO_MAX)
            logging.debug("update servo key : " + str(msg) + " target :" + str(self.target_pos))
            self.self_pwm_channels.servo[self.SERVO_POS].angle = self.target_pos

    """def animate(self):
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
            logging.error("servo step : " + str(step) + " out of range")"""
