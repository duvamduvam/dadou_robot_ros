import logging
import logging.config
import logging.config
import os
import time
import unittest

from adafruit_servokit import ServoKit

from dadou_utils_ros.logging_conf import LoggingConf
from dadou_utils_ros.utils.time_utils import TimeUtils
from dadou_utils_ros.utils_static import NECK, LEFT_ARM, RIGHT_ARM, RIGHT_EYE, LEFT_EYE, MODE, \
    SINGLE_THREAD, LOGGING_TEST_FILE_NAME, RANDOM, RANDOM_MOVE_MIN, RANDOM_MOVE_MAX, RANDOM_TIME_MIN, RANDOM_TIME_MAX, \
    RANDOM_DURATION, LEFT_ARM_NB, HEAD_PWM_NB, RIGHT_ARM_NB, LEFT_EYE_NB, RIGHT_EYE_NB
from robot.actions import Servo
from robot.input.global_receiver import GlobalReceiver
from robot.robot_config import config


class ServosTests(unittest.TestCase):
    print(os.getcwd())
    logging.config.dictConfig(LoggingConf.get(config[LOGGING_TEST_FILE_NAME], "tests"))

    config[SINGLE_THREAD] = True
    receiver = GlobalReceiver(config, None)
    neck = Servo(NECK, config[HEAD_PWM_NB], 99, 180, True, True, receiver)
    left_arm = Servo(LEFT_ARM, config[LEFT_ARM_NB], 99, 180, True, True, receiver)
    right_arm = Servo(RIGHT_ARM, config[RIGHT_ARM_NB], 99, 180, True, True, receiver)
    left_eye = Servo(LEFT_EYE, config[LEFT_EYE_NB], 99, 180, True, True, receiver)
    right_eye = Servo(RIGHT_EYE, config[RIGHT_EYE_NB], 99, 180, True, True, receiver)



    def test_neck(self):
        logging.debug("start test neck")

        for i in range(3):
            self.neck.update({NECK: 180})
            time.sleep(5)
            self.neck.update({NECK: 80})
            time.sleep(5)
            self.neck.update({NECK: 50})
            time.sleep(5)

    def test_random_neck(self):
        self.neck.update({NECK: {MODE: RANDOM, RANDOM_DURATION: 30000, RANDOM_MOVE_MIN: 35, RANDOM_MOVE_MAX: 75, RANDOM_TIME_MIN: 500, RANDOM_TIME_MAX: 3000}})
        start_time = TimeUtils.current_milli_time()
        while not TimeUtils.is_time(start_time, 30000):
            self.neck.process()

    def test_left_arm(self):
        logging.debug("start test left arm")

        for i in range(3):
            self.left_arm.update({LEFT_ARM: 0})
            time.sleep(10)
            self.left_arm.update({LEFT_ARM: 120})
            time.sleep(10)
            #self.left_arm.update({LEFT_ARM: 10})
            #time.sleep(5)
            #self.left_arm.update({LEFT_ARM: 170})
            #time.sleep(5)

    def test_right_arm(self):
        logging.debug("start test left arm")

        for i in range(3):
            self.right_arm.update({RIGHT_ARM: 0})
            time.sleep(10)
            self.right_arm.update({RIGHT_ARM: 360})
            time.sleep(10)
            #self.right_arm.update({RIGHT_ARM: 10})
            #time.sleep(5)
            #self.right_arm.update({RIGHT_ARM: 170})
            #time.sleep(5)


    def test_eyes(self):
        logging.debug("start test left eye")

        for i in range(3):
            self.right_eye.update({RIGHT_EYE: 0})
            self.left_eye.update({LEFT_EYE: 99})
            time.sleep(5)
            self.right_eye.update({RIGHT_EYE: 99})
            self.left_eye.update({LEFT_EYE: 0})
            time.sleep(5)
            self.right_eye.update({RIGHT_EYE: 0})
            self.left_eye.update({LEFT_EYE: 99})
            time.sleep(5)
            self.right_eye.update({RIGHT_EYE: 50})
            self.left_eye.update({LEFT_EYE: 50})
            time.sleep(5)

    def test_move_arms(self):
        for i in range(3):
            self.right_arm.update({RIGHT_ARM: 99})
            self.left_arm.update({LEFT_ARM: 99})
            time.sleep(10)
            self.right_arm.update({RIGHT_ARM: 70})
            self.left_arm.update({LEFT_ARM: 70})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 60})
            self.left_arm.update({LEFT_ARM: 60})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 50})
            self.left_arm.update({LEFT_ARM: 50})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 0})
            self.left_arm.update({LEFT_ARM: 0})
            time.sleep(10)

    def test_random_eyes(self):
        for i in range(3):
            self.right_eye.update({RIGHT_EYE: {MODE: RANDOM, RANDOM_DURATION: 30000, RANDOM_MOVE_MIN: 10, RANDOM_MOVE_MAX: 95, RANDOM_TIME_MIN: 500, RANDOM_TIME_MAX: 3000}})
            self.left_eye.update({LEFT_EYE: {MODE: RANDOM, RANDOM_DURATION: 30000, RANDOM_MOVE_MIN: 20, RANDOM_MOVE_MAX: 99, RANDOM_TIME_MIN: 100, RANDOM_TIME_MAX: 2000}})
            start_time = TimeUtils.current_milli_time()
            while not TimeUtils.is_time(start_time, 30000):
                self.right_eye.process()
                self.left_eye.process()

    def test_random_arms(self):
        for i in range(3):
            self.right_arm.update({RIGHT_ARM: {MODE: RANDOM, RANDOM_DURATION: 30000, RANDOM_MOVE_MIN: 55, RANDOM_MOVE_MAX: 95, RANDOM_TIME_MIN: 500, RANDOM_TIME_MAX: 3000}})
            self.left_arm.update({LEFT_ARM: {MODE: RANDOM, RANDOM_DURATION: 30000, RANDOM_MOVE_MIN: 60, RANDOM_MOVE_MAX: 99, RANDOM_TIME_MIN: 100, RANDOM_TIME_MAX: 2000}})
            start_time = TimeUtils.current_milli_time()
            while not TimeUtils.is_time(start_time, 30000):
                self.right_arm.process()
                self.left_arm.process()

    def test_move_arms_neck(self):
        for i in range(3):
            self.right_arm.update({RIGHT_ARM: 0})
            self.left_arm.update({LEFT_ARM: 0})
            self.neck.update({NECK: 0})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 120})
            self.left_arm.update({LEFT_ARM: 120})
            self.neck.update({NECK: 120})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 10})
            self.left_arm.update({LEFT_ARM: 10})
            self.neck.update({NECK: 10})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 170})
            self.left_arm.update({LEFT_ARM: 170})
            self.neck.update({NECK: 170})
            time.sleep(5)

    def test_servokit(self):
        kit = ServoKit(channels=16)

        # Below desides the initial angle that the servo which is attatched to Port 0 will be. In this case we will make it zero degrees.
        # kit.servo[0].angle = 0
        # kit.frequency(60)
        # Below will create an infinite loop
        for i in range(3):
            kit.servo[4].angle = 0
            time.sleep(5)

            kit.servo[4].angle = 180
            time.sleep(5)


if __name__ == '__main__':
    unittest.main()
