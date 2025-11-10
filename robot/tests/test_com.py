import unittest

class JenkinsTestCase(unittest.TestCase):

    def test_true(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_false(self):
        self.assertEqual('foo'.upper(), 'boo')