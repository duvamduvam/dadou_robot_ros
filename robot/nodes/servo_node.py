#!/usr/bin/env python3
import json
import logging
import logging.config
import time

import rclpy
from rclpy.node import Node
from robot_interfaces.msg._string_time import StringTime

from dadou_utils_ros.logging_conf import LoggingConf
from dadou_utils_ros.utils_static import NECK, HEAD_PWM_NB, DEFAULT_POS, I2C_ENABLED, PWM_CHANNELS_ENABLED, \
    SERVOS, MAX_POS, SERVO, NAME, LOGGING_FILE_NAME, DURATION
from robot.actions.servo import Servo
from robot.robot_config import config


class ServosNode(Node):
    def __init__(self):

        super().__init__("servo_node")

        self.declare_parameter(NAME, rclpy.Parameter.Type.STRING)
        self.declare_parameter(HEAD_PWM_NB, rclpy.Parameter.Type.INTEGER)
        self.declare_parameter(DEFAULT_POS, rclpy.Parameter.Type.INTEGER)
        self.declare_parameter(MAX_POS, rclpy.Parameter.Type.INTEGER)

        self.servo_type = self.get_parameter(NAME).get_parameter_value().string_value
        servo_pwm_nb = self.get_parameter(HEAD_PWM_NB).get_parameter_value().integer_value
        servo_default_pos = self.get_parameter(DEFAULT_POS).get_parameter_value().integer_value
        servo_max = self.get_parameter(MAX_POS).get_parameter_value().integer_value

        logging.config.dictConfig(LoggingConf.get(config[LOGGING_FILE_NAME], self.servo_type))

        logging.info("Starting {} on pwm channel {} default servo pos {} max servo pos {}".format(
            self.servo_type, servo_pwm_nb, servo_default_pos, servo_max))

        self.servo = Servo(servo_type=self.servo_type, pwm_channel_nb=servo_pwm_nb, default_pos=servo_default_pos,
                           servo_max=servo_max, i2c_enabled=config[I2C_ENABLED],
                           pwm_channels_enabled=config[PWM_CHANNELS_ENABLED])

        self.subscription = self.create_subscription(
            StringTime,
            self.servo_type,
            self.listener_callback,
            10)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def listener_callback(self, ros_msg):
        msg = json.loads(ros_msg.msg)
        duration = ros_msg.time
        action_msg = {self.servo_type: msg}
        if ros_msg.time != 0:
            action_msg[DURATION] = ros_msg.time
        logging.info("{} input {} : ".format(self.servo_type, ros_msg))
        self.servo.update(action_msg)

    def timer_callback(self):
        try:
            self.servo.process()
        except Exception as e:
            logging.error(e, exc_info=True)


def main(args=None):
    rclpy.init(args=args)
    node = ServosNode()
    try:
        rclpy.spin(node)
    except Exception as e:
        logging.error(e, exc_info=True)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
