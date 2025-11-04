import unittest

from dadoucontrol import Com
from dadoucontrol import Utils
from tests import TestSetup

TestSetup()


class JenkinsTestCase(unittest.TestCase):
    com = Com()

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
