import time
import unittest
import logging

from head import Head


class Servo(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    head = Head()

    def test_move_key(self):
        for i in range(10):
            key = '!'
            self.head.update(key)
            self.head.process()
            time.sleep(5)
            key = '~'
            self.head.update(key)
            self.head.process()
            time.sleep(5)

