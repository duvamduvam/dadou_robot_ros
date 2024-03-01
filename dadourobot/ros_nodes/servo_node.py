#!/usr/bin/env python3
import logging
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from dadou_utils.utils_static import ROBOT_MSG, NECK, HEAD_PWM_NB, DEFAULT_POS
from dadourobot.actions.servo import Servo
from dadourobot.actions.wheel import Wheel
from dadourobot.robot_config import config


class ServosNode(Node):
    def __init__(self):
        super().__init__("node_name")
        self.servo = Wheel(config)

        servo_type = self.get_param(NECK, 10)
        servo_pwm_nb = self.get_param(HEAD_PWM_NB, 10)
        servo_default_pos = self.get_param(config[DEFAULT_POS], 10)

        self.servo = Servo(NECK, config[HEAD_PWM_NB], 57, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver)

        #components.append(Servo(NECK, config[HEAD_PWM_NB], 57, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        #components.append(Servo(LEFT_EYE, config[LEFT_EYE_NB], 70, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        #components.append(Servo(RIGHT_EYE, config[RIGHT_EYE_NB], 45, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        #components.append(Servo(LEFT_ARM, config[LEFT_ARM_NB], 99, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        #components.append(Servo(RIGHT_ARM, config[RIGHT_ARM_NB], 160, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))


        self.subscriber_ = self.create_subscription(String, ROBOT_MSG, self.robot_news_callback, 10)
        self.get_logger().info("smartphone have been started")

    def robot_news_callback(self, msg):
        self.get_logger().info(msg.data)
        self.servo.update(msg.data)

    def run(self):
        while True:
            try:
                self.servo.process()
                time.sleep(0.001)
            except Exception as err:
                logging.error('exception {}'.format(err), exc_info=True)

def main(args=None):
    rclpy.init(args=args)
    node = ServosNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
