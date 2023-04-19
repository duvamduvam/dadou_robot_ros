import os

import adafruit_pca9685
import board
import busio
from adafruit_servokit import ServoKit
from dadou_utils.utils_static import WHEEL_LEFT, WHEEL_RIGHT, HEAD_PWM_NB

from dadourobot.robot_config import config
from dadourobot.files.robot_json_manager import RobotJsonManager
from dadourobot.tests.conf_test import TestSetup

TestSetup()

import time
import unittest


class PWMMotorTest(unittest.TestCase):
    TestSetup()

    #kit = ServoKit(channels=16)

    #kit.servo[15].set_pulse_width_range(1000, 2000)
    #kit.servo[14].set_pulse_width_range(1000, 2000)
    #kit.frequency = 60

    MAX = 65535
    i2c = busio.I2C(board.SCL, board.SDA)
    pca9685 = adafruit_pca9685.PCA9685(i2c)
    pca9685.frequency = 60

    pwm_motor1 = pca9685.channels[1]
    pwm_motor1.duty_cycle = 0

    dir_motor1 = pca9685.channels[0]
    dir_motor1.duty_cycle = 0

    pwm_motor2 = pca9685.channels[2]
    pwm_motor2.duty_cycle = 0

    dir_motor2 = pca9685.channels[3]
    dir_motor2.duty_cycle = 0

    neck = pca9685.channels[config[HEAD_PWM_NB]]
    neck.duty_cycle = 0

    def test_left_run(self):
        self.dir_motor1.duty_cycle = self.MAX
        self.pwm_motor1.duty_cycle = 10000
        time.sleep(15)
        self.dir_motor1.duty_cycle = 0
        self.pwm_motor1.duty_cycle = 10000
        time.sleep(15)
        self.pwm_motor1.duty_cycle = 0

    def test_neck_run(self):
        for i in range(3):
            self.neck.duty_cycle = 0
            self.neck.duty_cycle = 10000
            time.sleep(5)

    def test_both(self):
        self.dir_motor1.duty_cycle = 0
        self.increase_decrease(self.pwm_motor1)
        self.dir_motor1.duty_cycle = self.MAX
        self.increase_decrease(self.pwm_motor1)
        self.pwm_motor1.duty_cycle = 0

        self.dir_motor2.duty_cycle = 0
        self.increase_decrease(self.pwm_motor2)
        self.dir_motor2.duty_cycle = self.MAX
        self.increase_decrease(self.pwm_motor2)
        self.pwm_motor2.duty_cycle = 0

    def increase_decrease(self, pwm):
        for i in range(5000, 25000, 2):
            pwm.duty_cycle = i

        #    # Decrease brightness:
        for i in range(25000, 5000, -2):
            pwm.duty_cycle = i

        #for w in range(0, 4):

            #self.pwm_motor1.duty_cycle = 10000
            #self.dir_motor1.duty_cycle = 0
            #time.sleep(5)

            #self.pwm_motor1.duty_cycle = 10000
            #self.dir_motor1.duty_cycle = 0
            #self.pwm_motor2.duty_cycle = 10000
            #self.dir_motor2.duty_cycle = 0
            #time.sleep(5)

            #self.pwm_motor1.duty_cycle = 30000
            #self.dir_motor1.duty_cycle = self.MAX
            #self.pwm_motor2.duty_cycle = 30000
            #self.dir_motor2.duty_cycle = self.MAX
            #time.sleep(5)

            #self.pwm_motor1.duty_cycle = 0
            #self.pwm_motor2.duty_cycle = 0

            # Increase brightness:
            #for i in range(20000):
            #    self.pwm_motor1.duty_cycle = i

        #    # Decrease brightness:
            #for i in range(20000, 0, -1):
            #    self.pwm_motor1.duty_cycle = i


if __name__ == '__main__':
    unittest.main()
