import logging.config
from dadourobot.tests.conf_test import TestSetup
TestSetup()

import time
import unittest
import logging
import logging.config

from dadoucontrol import Neck


class NeckTests(unittest.TestCase):
    TestSetup()

    neck = Neck()

    def test_move_key(self):
        logging.debug("start test servo")
        for i in range(3):
            logging.debug("test key 60 for servo")
            self.neck.update(40)
            self.neck.process()
            time.sleep(1)
            self.neck.process()
            time.sleep(1)
            self.neck.process()
            time.sleep(1)
            self.neck.process()
            time.sleep(5)
            logging.debug("test key 130 for servo")
            self.neck.update(100)
            self.neck.process()
            time.sleep(1)
            self.neck.process()
            time.sleep(1)
            self.neck.process()
            time.sleep(1)
            self.neck.process()
            time.sleep(5)


if __name__ == '__main__':
    unittest.main()
