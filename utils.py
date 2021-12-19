import time
import logging
from numpy import interp


class Utils:
    first_char_nb = 33
    last_char_nb = 126
    pwm_min = 0
    pwm_max = 180

    def translate(self, value):
        return Utils.translate5(value, self.first_char_nb, self.last_char_nb, self.pwm_min, self.pwm_max)

    def translate3(self, value, left_min, left_max, ):
        return Utils.translate5(value, left_min, left_max, self.pwm_min, self.pwm_man)

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

    @staticmethod
    def current_milli_time():
        return round(time.time() * 1000)

    def is_positive(self, value):
        value > (self.last_char - self.first_char)

    @staticmethod
    def is_time(last_time, time_out) -> bool:
        current = round(time.time() * 1000)
        is_time = (current - last_time) + time_out
        logging.info("last time: " + str(last_time)+" current time : " + str(current) +
                     " time step : " + str(time_out) + " is time : " + str(is_time))
        return is_time
