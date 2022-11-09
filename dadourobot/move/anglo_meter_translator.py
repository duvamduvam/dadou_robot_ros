import logging
import math

from dadou_utils.misc import Misc


class AngloMeterTranslator:

    MIN_JOYSTICK = 0
    MAX_JOYSTICK = 99
    MIN_INPUT = -100
    MAX_INPUT = 100

    INVERSE = 5
    UP_ANGLE_MARGIN = 10
    DOWN_ANGLE_MARGIN = 80

    def translate(self, command:str):
        turn = int(command[0:2])
        forward = int(command[2:4])

        differential =  self.axis_to_diff(turn, forward, self.MIN_JOYSTICK, self.MAX_JOYSTICK, self.MIN_INPUT, self.MAX_INPUT)
        logging.info("translate turn {} forward {} to {}".format(turn, forward, differential))
        return differential

    def axis_to_diff2(self, x, y)->(int, int):

        left, right = 0, 0

        angle = int(math.degrees(math.atan(x/y)))
        logging.debug("angle : {}".format(angle))

        # differential 90° / 0 <-> 1 / 0  + facteur exponential * x
        # INVERSE / angle * right or left
        if y >= 0:
            left = Misc.mapping(x, 0, 1024, 0, 100)
            right = self.create_differential(angle, left)
        else:
            right = Misc.mapping(x, 0, 1024, 0, 100)
            left = self.create_differential(angle, right)

        logging.info("x {} y {} -> left {} right {}".format(x, y, left, right))
        return left, right

    def create_differential(self, angle, side):
        if angle <= self.INVERSE or angle <= self.DOWN_ANGLE_MARGIN:
            return 0
        if angle >= self.UP_ANGLE_MARGIN:
            return 1

        int(side * (self.INVERSE / angle))

    def axis_to_diff(self, x, y, min_joystick, max_joystick, min_speed, max_speed):
        if x == 0 and y == 0:
            return (0, 0)

        # First Compute the angle in deg
        # First hypotenuse
        z = math.sqrt(x * x + y * y)

        # angle in radians
        rad = math.acos(math.fabs(x) / z)

        # and in degrees
        angle = rad * 180 / math.pi

        # Now angle indicates the measure of turn
        # Along a straight line, with an angle o, the turn co-efficient is same
        # this applies for angles between 0-90, with angle 0 the coeff is -1
        # with angle 45, the co-efficient is 0 and with angle 90, it is 1

        tcoeff = -1 + (angle / 90) * 2
        turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
        turn = round(turn * 100, 0) / 100

        # And max of y or x is the movement
        mov = max(math.fabs(y), math.fabs(x))

        # First and third quadrant
        if (x >= 0 and y >= 0) or (x < 0 and y < 0):
            rawLeft = mov
            rawRight = turn
        else:
            rawRight = mov
            rawLeft = turn

        # Reverse polarity
        if y < 0:
            rawLeft = 0 - rawLeft
            rawRight = 0 - rawRight

        # minJoystick, maxJoystick, minSpeed, maxSpeed
        # Map the values onto the defined rang
        rightOut = Misc.mapping(rawRight, min_joystick, max_joystick, min_speed, max_speed)
        leftOut = Misc.mapping(rawLeft, min_joystick, max_joystick, min_speed, max_speed)

        return (int(rightOut), int(leftOut))

    @staticmethod
    def mapping(self, v, in_min, in_max, out_min, out_max):
        # Check that the value is at least in_min
        if v < in_min:
            v = in_min
        # Check that the value is at most in_max
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min