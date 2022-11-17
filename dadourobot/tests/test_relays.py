import board
import digitalio

import time
import unittest
from microcontroller import Pin
from digitalio import DigitalInOut, Direction


class TestRelays(unittest.TestCase):

    def test_direct(self):
        relay = DigitalInOut(board.D5)
        relay.direction = Direction.OUTPUT

        relay_on = False

        for x in range(0, 50):

            print("switch "+str(relay_on))
            relay.value = relay_on
            relay_on = not relay_on
            time.sleep(5)

