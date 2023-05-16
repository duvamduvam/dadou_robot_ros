import logging.config
import sys
import time
import unittest
import logging
import logging.config

from adafruit_servokit import ServoKit

from dadourobot.actions.left_arm import LeftArm
from dadourobot.actions.left_eye import LeftEye
from dadourobot.actions.neck import Neck

from dadou_utils.utils_static import NECK, LEFT_ARM, RIGHT_ARM, LOGGING_CONFIG_TEST_FILE, RIGHT_EYE, LEFT_EYE

from dadourobot.actions.right_arm import RightArm
from dadourobot.actions.right_eye import RightEye
from dadourobot.robot_config import config
from dadourobot.tests.conf_test import TestSetup



class NeckTests(unittest.TestCase):
    TestSetup()
    neck = Neck(config)
    left_arm = LeftArm(config)
    right_arm = RightArm(config) #setup.right_arm
    left_eye = LeftEye(config)
    right_eye = RightEye(config)

    def test_neck(self):
        logging.debug("start test neck")

        for i in range(3):
            self.neck.update({NECK: 0})
            time.sleep(5)
            self.neck.update({NECK: 50})
            time.sleep(5)
            self.neck.update({NECK: 80})
            time.sleep(5)


    def test_left_arm(self):
        logging.debug("start test left arm")

        for i in range(3):
            self.left_arm.update({LEFT_ARM: 0})
            time.sleep(5)
            self.left_arm.update({LEFT_ARM: 120})
            time.sleep(5)
            self.left_arm.update({LEFT_ARM: 10})
            time.sleep(5)
            self.left_arm.update({LEFT_ARM: 170})
            time.sleep(5)

    def test_right_arm(self):
        logging.debug("start test left arm")

        for i in range(3):
            self.right_arm.update({RIGHT_ARM: 0})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 120})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 10})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 170})
            time.sleep(5)


    def test_eyes(self):
        logging.debug("start test left eye")

        for i in range(3):
            self.right_eye.update({RIGHT_EYE: 0})
            self.left_eye.update({LEFT_EYE: 180})
            time.sleep(5)
            self.right_eye.update({RIGHT_EYE: 120})
            self.left_eye.update({LEFT_EYE: 120})
            time.sleep(5)
            self.right_eye.update({RIGHT_EYE: 10})
            self.left_eye.update({LEFT_EYE: 10})
            time.sleep(5)
            self.right_eye.update({RIGHT_EYE: 170})
            self.left_eye.update({LEFT_EYE: 0})
            time.sleep(5)


    def test_move_arms(self):
        for i in range(3):
            self.right_arm.update({RIGHT_ARM: 0})
            self.left_arm.update({LEFT_ARM: 0})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 120})
            self.left_arm.update({LEFT_ARM: 120})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 10})
            self.left_arm.update({LEFT_ARM: 10})
            time.sleep(5)
            self.right_arm.update({RIGHT_ARM: 170})
            self.left_arm.update({LEFT_ARM: 170})
            time.sleep(5)
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
