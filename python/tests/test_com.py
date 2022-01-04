import logging
import unittest

from python.com import Com
from python.tests.conf_test import TestSetup
from python.utils import Utils

TestSetup()


class MyTestCase(unittest.TestCase):
    com = Com()

    def test_com(self):
        start_time = Utils.current_milli_time()
        while True:
            msg = self.com.get_msg()
            if msg:
                logging.info("new msg : " + msg)
