import logging
import unittest

from python.input.com import Com
from python.tests.conf_test import TestSetup
from python.utils import Utils

TestSetup()


class MyTestCase(unittest.TestCase):
    com = Com()

    def test_com(self):
        start_time = Utils.current_milli_time()
        while True:
            self.com.get_msg()
