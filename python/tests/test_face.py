import logging.config

from python.actions.face import Face
from python.tests.conf_test import TestSetup

import unittest


class MyTestCase(unittest.TestCase):


    def test_load_visual(self):
        Face()


if __name__ == '__main__':
    unittest.main()
