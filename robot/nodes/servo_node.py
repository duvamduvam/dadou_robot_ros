#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from dadou_utils.utils_static import ROBOT_MSG, NECK, HEAD_PWM_NB, DEFAULT_POS, I2C_ENABLED, PWM_CHANNELS_ENABLED, \
    SERVOS, MAX_POS
from robot.actions.servo import Servo
from robot.actions.wheels import Wheels
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class ServosNode(SubscriberNode):
    def __init__(self):
        self.servo = Wheel(config)

        servo_type = self.get_param(NECK, 10)
        servo_pwm_nb = self.get_param(HEAD_PWM_NB, 10)
        servo_default_pos = self.get_param(DEFAULT_POS, 10)
        servo_max = self.get_param(MAX_POS, 10)
        i2c_enabled = self.get_param(I2C_ENABLED, 10)
        pwm_channels_enabled = self.get_param(PWM_CHANNELS_ENABLED, 10)

        self.servo = Servo(type=servo_type, pwm_channel_nb=servo_pwm_nb, default_pos=servo_default_pos, servo_max=servo_max, i2c_enabled=i2c_enabled,
                           pwm_channels_enabled=pwm_channels_enabled)

        super().__init__(SERVOS + "_node", SERVOS, self.servo)
def main(args=None):
    rclpy.init(args=args)
    node = ServosNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
