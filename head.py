from utils import Utils
import pwmio
import board
import logging


class Head:
    target_pos, current_pos, target, servo_min = 0
    servo_max = 180
    margin = 5

    head_pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
        #pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)

    def update(self, key: chr):
        self.target = self.utils.translate(key)

    def process(self):

        diff = abs(self.target_pos - self.current_pos);
        if diff > self.margin and self.target_pos != self.current_pos:
            if self.target_pos > self.current_pos:
                self.next_step(1)
            else:
                self.next_step(-1)

    def next_step(self, step):
        if self.servo_min <= self.current_pos <= self.servo_max:
            logging.info ("position "+self.current_pos+" next step "+step);
            self.current_pos += step;
            self.head_pwm.angle(self.current_pos)
