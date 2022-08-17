import time
import logging
from numpy import interp


class Utils:
    first_char = 33
    last_char = 126
    pwm_min = 0
    pwm_max = 180

    def translate(self, value):
        return int(Utils.translate5(ord(value), self.first_char, self.last_char, self.pwm_min, self.pwm_max))

    def translate3(self, value, left_min, left_max, ):
        return Utils.translate5(value, left_min, left_max, self.pwm_min, self.pwm_max)

    @staticmethod
    def translate5(value, left_min, left_max, right_min, right_max) -> int:
        # Figure out how 'wide' each range is
        # left_span = left_max - left_min
        # right_span = right_max - right_min

        # Convert the left range into a 0-1 range (float)
        # value_scaled = float(value - left_min) / float(left_max)

        # Convert the 0-1 range into a value in the right range.
        return interp(value, [left_min, left_max], [right_min, right_max])
        # return abs(right_min + (value_scaled * right_span))


    def is_positive(self, value: int) -> bool:
        return value > (self.last_char - self.first_char)

    @staticmethod
    def last_line(file) -> str:
        with open(file) as f:
            return f.readlines()[-1]
