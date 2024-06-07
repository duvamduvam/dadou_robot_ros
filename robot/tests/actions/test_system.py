
import logging
import logging.config
import unittest
import board

from dadou_utils_ros.logging_conf import LoggingConf
from dadou_utils_ros.utils.status import Status
from dadou_utils_ros.utils_static import LOGGING_TEST_FILE_NAME
from robot.robot_config import config


class TestSystem(unittest.TestCase):

    logging.config.dictConfig(LoggingConf.get(config[LOGGING_TEST_FILE_NAME], "test_face"))
    system = Status(config)

    print(dir(board))

    def test_status(self):

        while True:
            self.system.process()


if __name__ == '__main__':
    unittest.main()
