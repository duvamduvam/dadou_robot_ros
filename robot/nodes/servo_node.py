#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from dadou_utils_ros.utils_static import NECK, HEAD_PWM_NB, DEFAULT_POS, I2C_ENABLED, PWM_CHANNELS_ENABLED, \
    SERVOS, MAX_POS, SERVO, NAME
from robot.actions.servo import Servo
from robot.actions.wheels import Wheels
from robot.nodes.abstract_subscriber import SubscriberNode
from robot.robot_config import config


class ServosNode(Node):
    def __init__(self):
        super().__init__("servo_node")

        self.declare_parameter(NAME, rclpy.Parameter.Type.STRING)
        self.declare_parameter(HEAD_PWM_NB, rclpy.Parameter.Type.INTEGER)
        self.declare_parameter(DEFAULT_POS, rclpy.Parameter.Type.INTEGER)
        self.declare_parameter(MAX_POS, rclpy.Parameter.Type.INTEGER)

        servo_type = self.get_parameter(NAME).get_parameter_value().string_value
        servo_pwm_nb = self.get_parameter(HEAD_PWM_NB).get_parameter_value().integer_value
        servo_default_pos = self.get_parameter(DEFAULT_POS).get_parameter_value().integer_value
        servo_max = self.get_parameter(MAX_POS).get_parameter_value().integer_value

        self.get_logger().info("Starting {} on pwm channel {} default servo pos {} max servo pos {}".format(
            servo_type, servo_pwm_nb, servo_default_pos, servo_max))

        self.servo = Servo(type=servo_type, pwm_channel_nb=servo_pwm_nb, default_pos=servo_default_pos,
                           servo_max=servo_max, i2c_enabled=config[I2C_ENABLED],
                           pwm_channels_enabled=config[PWM_CHANNELS_ENABLED])

        self.get_logger().info("Starting {}".format(servo_type))

        self.subscription = self.create_subscription(
            String,
            servo_type,
            self.listener_callback,
            10)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def listener_callback(self, ros_msg):
        msg = ros_msg.data
        self.get_logger().info('I heard: "%s"' % msg)
        self.servo.update({ self.action_type: msg})
    def timer_callback(self):
        # Logique à exécuter en continu ici
        self.get_logger().debug('Action en temps réel')
        self.servo.process()

def main(args=None):
    rclpy.init(args=args)
    node = ServosNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
