import logging
import math

from dadou_utils.misc import Misc
from dadourobot.robot_config import MAX_PWM_R

MIN_JOYSTICK = -99
MAX_JOYSTICK = 99
# MIN_INPUT = -100
# MAX_INPUT = 100

INVERSE = 5
UP_ANGLE_MARGIN = 10
DOWN_ANGLE_MARGIN = 80

left_motor_output = 0 # will hold the calculated output for the left motor
right_motor_output = 0 # will hold the calculated output for the right motor


class AngloMeterTranslator:

    def translate(self, forward, turn):
        left, right = self.calculate_diff(turn, forward)
        #logging.info("translate turn {} forward {} to left {} right {}".format(turn, forward, left, right))
        return left, right

    def calculate_diff(self, x, y):

        # first Compute the angle in deg
        # First hypotenuse
        z = math.sqrt(x * x + y * y)

        # angle in radians
        rad = math.acos(abs(x) / z) if z != 0 else 0  # Cataer for NaN values

        # and in degrees
        angle = rad * 180 / math.pi

        # Now angle indicates the measure of turn
        # Along a straight line, with an angle o, the turn co-efficient is same
        # this applies for angles between 0-90, with angle 0 the co-eff is -1
        # with angle 45, the co-efficient is 0 and with angle 90, it is 1

        tcoeff = -1 + (angle / 90) * 2
        turn = tcoeff * abs(abs(y) - abs(x))
        turn = round(turn * 100) / 100

        # And max of y or x is the movement
        mov = max(abs(y), abs(x))

        # First and third quadrant
        if (x >= 0 and y >= 0) or (x < 0 and y < 0):
            left = mov
            right = turn
        else:
            right = mov
            left = turn

        # Reverse polarity
        if y < 0:
            left = 0 - left
            right = 0 - right

        # Map the values onto the defined range
        left_motor_output = int(Misc.mapping(left, MIN_JOYSTICK, MAX_JOYSTICK, -100, 100))
        right_motor_output = int(Misc.mapping(right, MIN_JOYSTICK, MAX_JOYSTICK, -100, 100))

        #return left, right
        return left_motor_output, right_motor_output
