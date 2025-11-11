import os
import time
import unittest

RUN_HARDWARE_TESTS = os.getenv("RUN_HARDWARE_TESTS") == "1"
HARDWARE_IMPORT_ERROR = None

if RUN_HARDWARE_TESTS:
    try:
        import adafruit_pcf8574
        import board
        from digitalio import DigitalInOut, Direction
    except Exception as exc:  # pragma: no cover - best effort for headless CI
        HARDWARE_IMPORT_ERROR = exc
        adafruit_pcf8574 = board = DigitalInOut = Direction = None
else:
    HARDWARE_IMPORT_ERROR = RuntimeError(
        "Hardware relays tests disabled; set RUN_HARDWARE_TESTS=1 to run them."
    )
    adafruit_pcf8574 = board = DigitalInOut = Direction = None


@unittest.skipIf(
    HARDWARE_IMPORT_ERROR is not None,
    f"Hardware dependencies unavailable: {HARDWARE_IMPORT_ERROR}",
)
class TestRelays(unittest.TestCase):

    def test_kalxon(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        pcf = adafruit_pcf8574.PCF8574(i2c, address=0x21)
        self.test_reset()

        klaxon = pcf.get_pin(2)
        for x in range(0, 5):
            klaxon.value = False
            time.sleep(5)
            klaxon.value = True
