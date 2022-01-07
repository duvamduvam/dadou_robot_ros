from python.tests.conf_test import TestSetup
TestSetup()

import unittest

from python.tests.conf_test import TestSetup
from python.visual.visual import Image


class MyTestCase(unittest.TestCase):
    TestSetup()

    def test_load(self):
        image = Image("../../visuals/")
        image.load_images()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
