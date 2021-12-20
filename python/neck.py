import pwmio
import board
import logging
from adafruit_motor import servo
from python.utils import Utils


class Neck:
    target_pos = 0
    current_pos = 0
    target = 0
    servo_min = 0
    step = 10

    servo_max = 180
    margin = 5
    last_time = Utils.current_milli_time()
    time_step = 200

    utils = Utils()

    head_pwm = pwmio.PWMOut(board.D5, duty_cycle=2 ** 15, frequency=50)
    servo = servo.Servo(head_pwm)
        #pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)

    def update(self, key):
        self.target_pos = abs(self.utils.translate(key))
        logging.debug("update servo key : " + str(key) + " target :" + str(self.target))
        self.last_time = Utils.current_milli_time()

    def process(self):
        if Utils.is_time(self.last_time, self.time_step):
            diff = abs(self.target_pos - self.current_pos);
            logging.debug("servo target : " + str(self.target_pos) + " current : " + str(self.current_pos) +
                          " margin : " + str(self.margin));
            if diff > self.margin and self.target_pos != self.current_pos:
                if self.target_pos > self.current_pos:
                    self.next_step(self.step)
                else:
                    self.next_step(-self.step)

    def next_step(self, step):
        if self.servo_min <= self.current_pos <= self.servo_max:
            self.current_pos += step
            logging.info("next_step current position "+str(self.current_pos)+" next step "+str(step));
            self.servo.angle = self.current_pos
        else:
            logging.error("servo step : " + str(step) + " out of range")
