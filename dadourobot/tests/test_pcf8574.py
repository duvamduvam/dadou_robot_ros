import time
import unittest

import adafruit_pcf8574
import board


class TestPCF8574(unittest.TestCase):
    i2c = board.I2C()  # uses board.SCL and board.SDA
    pcf = adafruit_pcf8574.PCF8574(i2c)

    dir1 = pcf.get_pin(0)

    def test_something(self):
        for w in range(0, 5):
            self.dir1.value = True
            time.sleep(5)
            self.dir1.value = False
            time.sleep(5)


if __name__ == '__main__':
    unittest.main()
