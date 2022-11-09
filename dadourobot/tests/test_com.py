import unittest

from dadoucontrol import Com
from dadoucontrol.tests import TestSetup
from dadoucontrol import Utils

TestSetup()


class MyTestCase(unittest.TestCase):
    com = Com()

    def test_com(self):
        start_time = Utils.current_milli_time()
        while True:
            self.com.pop_msg()
