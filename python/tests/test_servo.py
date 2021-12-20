
import time
import unittest
import logging
import logging.config

from python.head import Head


class Servo(unittest.TestCase):
    logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

    head = Head()

    def test_move_key(self):
        head = Head()
        logging.debug("start test servo")
        for i in range(3):
            key = '!'
            logging.debug("test key 60 for servo")
            head.update(40)
            head.process()
            time.sleep(1)
            head.process()
            time.sleep(1)
            head.process()
            time.sleep(1)
            head.process()
            time.sleep(5)
            key = '~'
            logging.debug("test key 130 for servo")
            head.update(100)
            head.process()
            time.sleep(1)
            head.process()
            time.sleep(1)
            head.process()
            time.sleep(1)
            head.process()
            time.sleep(5)



if __name__ == '__main__':
    unittest.main()
