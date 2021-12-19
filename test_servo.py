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
            logging.debug("test key 60 for servo")
            self.head.update(60)
            self.head.process()
            time.sleep(5)
            key = '~'
            logging.debug("test key 130 for servo")
            self.head.update(130)
            self.head.process()
            time.sleep(5)



if __name__ == '__main__':
    unittest.main()
