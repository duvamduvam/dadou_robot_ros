#linux rpi install : sudo pip3 install Adafruit-Blinka
#sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka
import random
import time
import board
import neopixel
import logging.config
from rainbowio import colorwheel


class Lights:

    logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    BLACK = (0, 0, 0)

    # LED strip configuration:
    LED_COUNT = 64  # Number of LED pixels.
    LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 0  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

    strip = neopixel.NeoPixel(board.D18, LED_COUNT)
    strip.brightness = 0.1

    #strip = neopixel.NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    # strip.begin()

    # F Turns the NeoPixels red, green, and blue in sequence.
    def fade_red(self):
        self.strip.fill((255, 0, 0))
        time.sleep(0.5)
        self.strip.fill((0, 255, 0))
        time.sleep(0.5)
        self.strip.fill((0, 0, 255))
        time.sleep(0.5)

    def random(self):
        red = 0x100000
        i = random.randint(0, self.LED_COUNT)
        self.strip[i] = red

    def fill(self, color):
        logging.info("fill strip with "+str(color))
        self.strip.fill(color)

    def clean(self):
        self.strip.fill(self.BLACK)

    def color_chase(self, color, wait):
        for i in range(self.LED_COUNT):
            self.strip[i] = color
            time.sleep(wait)
            self.strip.show()
        time.sleep(0.5)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.LED_COUNT):
                rc_index = (i * 256 // self.LED_COUNT) + j
                self.strip[i] = colorwheel(rc_index & 255)
            self.strip.show()
            time.sleep(wait)


