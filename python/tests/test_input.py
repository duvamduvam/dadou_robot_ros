import logging.config
from python.tests.test_setup import TestSetup
TestSetup()
import random
import sys
import unittest

from python.file_watcher import FileWatcher
from python.tests.test_setup import TestSetup


class InputTest(unittest.TestCase):

    def test_key_file_watch(self):
        #file_path = '/home/david/Nextcloud/rosita/python/didier-python/conf/test_key.txt'
        #file_path = 'conf/test_key.txt'

        watcher = FileWatcher()
        key = str(random.randint(0, 99))
        watcher.add_key_to_file(key)

        self.assertTrue(watcher.changed())
        last_key = watcher.get_last_key()
        logging.info("last key : " + last_key)
        self.assertEqual(key, last_key, "keys don't match")
