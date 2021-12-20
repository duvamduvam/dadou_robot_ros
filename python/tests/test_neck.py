
import time
import unittest
import logging
import logging.config

from python.neck import Neck


class NeckTests(unittest.TestCase):
    logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

    neck = Neck()

    def test_move_key(self):
        logging.debug("start test servo")
        for i in range(3):
            key = '!'
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
            key = '~'
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
