import logging
import logging.config
import time
import unittest

from dadou_utils_ros.logging_conf import LoggingConf
from dadou_utils_ros.utils_static import LOGGING_TEST_FILE_NAME, TYPE
from robot.files.robot_json_manager import RobotJsonManager
from robot.robot_config import config
from robot.sequences.animation_manager import AnimationManager


class MyTestCase(unittest.TestCase):

    logging.config.dictConfig(LoggingConf.get(config[LOGGING_TEST_FILE_NAME], "test animation"))
    robot_json_manager = RobotJsonManager(config)
    animations_manager = AnimationManager(config, robot_json_manager)

    def test_random_type(self):
        self.animations_manager.update({TYPE:"bonjour"})
        while True:
            self.animations_manager.process()
            time.sleep(0.1)

