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

        differential =  self.axis_to_diff(turn, forward, MIN_JOYSTICK, MAX_JOYSTICK, 0, MAX_PWM_R )
        logging.info("translate turn {} forward {} to {}".format(turn, forward, differential))
        return differential

    def axis_to_diff2(self, x, y)->(int, int):
        angle = int(math.degrees(math.atan(x/y)))
        logging.debug("angle : {}".format(angle))

        # differential 90° / 0 <-> 1 / 0  + facteur exponential * x
        # INVERSE / angle * right or left
        if y >= 50:
            left = x #Misc.mapping(x, 0, 1024, 0, 100)
            right = self.create_differential(angle, left)
        else:
            right = x #Misc.mapping(x, 0, 1024, 0, 100)
            left = self.create_differential(angle, right)

        logging.info("x {} y {} -> left {} right {}".format(x, y, left, right))
        return left, right

    def create_differential(self, angle, side):
        if angle <= INVERSE or angle <= DOWN_ANGLE_MARGIN:
            return 0
        if angle >= UP_ANGLE_MARGIN:
            return 1

        int(side * (INVERSE / angle))

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

    def map_values(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


    def calculate_tank_drive(self, x, y):
        global left_motor_output, right_motor_output

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
            raw_left = mov
            raw_right = turn
        else:
            raw_right = mov
            raw_left = turn

        # Reverse polarity
        if y < 0:
            raw_left = 0 - raw_left
            raw_right = 0 - raw_right

        # Map the values onto the defined range
        left_motor_output = self.map_values(raw_left, MIN_JOYSTICK, MAX_JOYSTICK, 0, 100)
        right_motor_output = self.map_values(raw_right, MIN_JOYSTICK, MAX_JOYSTICK, 0, 100)

        return left_motor_output, right_motor_output

    def joystickToDiff(self, x, y):

        #x = self.translate(x, 0, 100, -100, 100)
        #y = self.translate(y, 0, 100, -100, 100)

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
        rightOut = self.map(rawRight, MIN_JOYSTICK, MAX_JOYSTICK, -100, 100)
        leftOut = self.map(rawLeft, MIN_JOYSTICK, MAX_JOYSTICK, -100, 100)

        #rightOut = self.translate(rightOut, -100, 100, 0, 100)
        #leftOut = self.translate(leftOut, -100, 100, 0, 100)

        return rightOut, leftOut

    def map(self, v, in_min, in_max, out_min, out_max):
        # Check that the value is at least in_min
        if v < in_min:
            v = in_min
        # Check that the value is at most in_max
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)