# pip3 install adafruit-circuitpython-servokit

from dadou_utils.utils_static import NECK, HEAD_PWM_NB, I2C_ENABLED, PWM_CHANNELS_ENABLED
from dadou_utils.actions.servo_abstract import ServoAbstract


MIN_PWM = 5000
MAX_PWM = 65530

DEFAULT_POS = 180


class Neck(ServoAbstract):

    SERVO_MIN = 0
    SERVO_MAX = 180
    DEFAULT_POS = 0

    def __init__(self, config):

        super().__init__(NECK, config[HEAD_PWM_NB], self.DEFAULT_POS, self.SERVO_MAX, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED])


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
