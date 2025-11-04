import logging.config
import time
import unittest
import logging
import logging.config

from dadou_utils_ros.com.input_messages_list import InputMessagesList
from dadou_utils_ros.utils.time_utils import TimeUtils

from robot.actions import LeftArm
from robot.actions import Neck

from dadou_utils_ros.utils_static import NECK, ANIMATION, KEY

from robot.actions import RightArm
from robot.input.global_receiver import GlobalReceiver
from robot.robot_factory import RobotFactory
from robot.tests.sandbox.conf_test import TestSetup
TestSetup()


class SequenceTests(unittest.TestCase):
    #setup = TestSetup()
     #setup.neck
     #setup.left_arm
    neck = Neck()
    left_arm = LeftArm()
    right_arm = RightArm() #setup.right_arm

    def test_neck(self):
        logging.debug("start test neck")

        for i in range(3):
            self.neck.update({NECK: 0})
            time.sleep(5)
            self.neck.update({NECK: 120})
            time.sleep(5)
            self.neck.update({NECK: 10})
            time.sleep(5)
            self.neck.update({NECK: 170})
            time.sleep(5)

    def test_sequence(self):

        self.process_sequence("D1", 500)

    def process_sequence(self, key, key_lunch_time):

        audio = RobotFactory().get_audio()
        face = RobotFactory().face
        # lights = RobotFactory().lights
        # lights = Lights(RobotFactory().get_strip())
        neck = RobotFactory().neck
        left_arm = RobotFactory().left_arm
        right_arm = RobotFactory().right_arm
        relays = RobotFactory().relays
        wheel = RobotFactory().wheel
        animations = RobotFactory().animation_manager

        global_receiver = GlobalReceiver(RobotFactory().device_manager, animations)

        start_time = TimeUtils.current_milli_time()
        msg_time = TimeUtils.current_milli_time()
        msg = None
        msg_sent = False
        input_messages = InputMessagesList()
        while True:

            if not msg_sent and TimeUtils.is_time(msg_time, key_lunch_time):
                msg_sent = True
                input_messages.add_msg({KEY: key})

            msg = global_receiver.get_msg()
            if msg and ANIMATION in msg and not msg[ANIMATION]:
                return

            if msg:
                audio.update(msg)
                neck.update(msg)
                left_arm.update(msg)
                right_arm.update(msg)
                face.update(msg)
                relays.update(msg)
                wheel.update(msg)
                # lights.update(msg)

                # if main_loop_sleep and main_loop_sleep != 0:
                #    time.sleep(main_loop_sleep)

            face.animate()
            # lights.animate()
            relays.process()
            wheel.check_stop(msg)
            # wheel.process()
            # neck.animate()


if __name__ == '__main__':
    unittest.main()
