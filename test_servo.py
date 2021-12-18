import time
import unittest
import logging

from head import Head


class Servo(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    head = Head()

    def move_key(self):
        for i in range(0, 10, 1):
            key = '!'
            self.head.update(key)
            time.sleep(5)
            key = '~'
            self.head.update(key)
            time.sleep(5)

