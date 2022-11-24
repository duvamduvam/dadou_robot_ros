import logging.config

from dadourobot.actions.neck import Neck
from dadourobot.config import RobotConfig
from dadou_utils.utils_static import NECK
from dadourobot.tests.conf_test import TestSetup
TestSetup()

import time
import unittest
import logging
import logging.config



class NeckTests(unittest.TestCase):
    setup = TestSetup()

    def test_move_key(self):
        logging.debug("start test servo")
        while True:
        #for i in range(3):
            logging.debug("test key 60 for servo")
            self.setup.neck.update({NECK:5})
            time.sleep(5)
            self.setup.neck.update({NECK:80})
            time.sleep(5)
            self.setup.neck.update({NECK:50})
            time.sleep(5)
            self.setup.neck.update({NECK:100})
            time.sleep(5)


if __name__ == '__main__':
    unittest.main()
