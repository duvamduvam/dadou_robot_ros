import time

# Import the RFM9x radio module.
import adafruit_rfm9x
import board
import busio
from digitalio import DigitalInOut

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D7)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

while True:
    # Attempt to set up the RFM9x Module
    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
        print('RFM9x: Detected')
    except RuntimeError as error:
        print('RFM9x Error: ', error)

    time.sleep(1)