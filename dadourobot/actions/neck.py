# pip3 install adafruit-circuitpython-servokit
import pwmio
import logging
from adafruit_motor import servo
from dadou_utils.time.time_utils import TimeUtils
from microcontroller import Pin

from dadourobot.robot_factory import RobotFactory
from dadourobot.utils import Utils


class Neck:
    target_pos = 0
    current_pos = 0
    servo_min = 0
    step = 10

    servo_max = 180
    servo_default = 50
    margin = 5
    last_time = TimeUtils.current_milli_time()
    time_step = 200

    utils = Utils()

    # pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)

    def __init__(self):
        config = RobotFactory().config
        self.head_pwm = pwmio.PWMOut(Pin(config.NECK_PIN), duty_cycle=2 ** 15, frequency=50)
        self.servo = servo.Servo(self.head_pwm)
        self.servo.angle = self.servo_default

    def update(self, msg):
        if msg:
            self.target_pos = abs(self.utils.translate(msg))
            logging.debug("update servo key : " + str(msg) + " target :" + str(self.target_pos))
            self.last_time = TimeUtils.current_milli_time()

    def animate(self):
        if TimeUtils.is_time(self.last_time, self.time_step):
            diff = abs(self.target_pos - self.current_pos)
            # logging.debug("servo target : " + str(self.target_pos) + " current : " + str(self.current_pos) +
            #              " margin : " + str(self.margin))
            if diff > self.margin and self.target_pos != self.current_pos:
                if self.target_pos > self.current_pos:
                    self.next_step(self.step)
                else:
                    self.next_step(-self.step)

    def next_step(self, step):
        if self.servo_min <= self.current_pos <= self.servo_max:
            self.current_pos += step
            logging.info("next_step current position " + str(self.current_pos) + " next step " + str(step))
            self.servo.angle = self.current_pos
        else:
            logging.error("servo step : " + str(step) + " out of range")
