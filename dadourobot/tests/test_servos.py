import logging.config
import time
import unittest
import logging
import logging.config

from adafruit_servokit import ServoKit

from dadourobot.actions.left_arm import LeftArm
from dadourobot.actions.neck import Neck

from dadou_utils.utils_static import NECK, LEFT_ARM, RIGHT_ARM, LOGGING_CONFIG_TEST_FILE

from dadourobot.actions.right_arm import RightArm
from dadourobot.robot_config import config
from dadourobot.tests.conf_test import TestSetup

TestSetup()


class NeckTests(unittest.TestCase):
    #setup = TestSetup()
     #setup.neck
     #setup.left_arm
    #logging.config.fileConfig(config[LOGGING_CONFIG_TEST_FILE], disable_existing_loggers=False)
    neck = Neck(config)
    left_arm = LeftArm(config)
    right_arm = RightArm(config) #setup.right_arm

    def test_neck(self):
        logging.debug("start test neck")

        for i in range(3):
            self.neck.update({NECK: 0})
            time.sleep(5)
            self.neck.update({NECK: 5})
            time.sleep(5)
            #self.neck.update({NECK: 90})
            #time.sleep(5)
            #self.neck.update({NECK: 180})
            #time.sleep(5)


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
