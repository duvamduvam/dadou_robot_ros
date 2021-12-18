import time
import unittest
import logging

from head import Head


class Servo(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    head = Head()

    def test_move_key(self):
        logging.debug("start test servo")
        for i in range(10):
            key = '!'
            logging.debug("test key ! for servo")
            self.head.update(key)
            self.head.process()
            time.sleep(500)
            key = '~'
            logging.debug("test key ~ for servo")
            self.head.update(key)
            self.head.process()
            time.sleep(500)

