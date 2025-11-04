import unittest

from dadoucontrol import Com
from dadoucontrol import Utils
from tests import TestSetup

TestSetup()


class JenkinsTestCase(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
