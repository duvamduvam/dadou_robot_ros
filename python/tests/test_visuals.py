import unittest
import logging
from python.visual import Image


class MyTestCase(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_load(self):
        image = Image("../../visuals/")
        image.load_images()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
