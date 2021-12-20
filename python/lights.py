#linux rpi install : sudo pip3 install Adafruit-Blinka
#sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka
import random
import time
import board
import neopixel


class Lights:

    pixel_nb = 250
    board.num_pixels = 250

    pixels = neopixel.NeoPixel(board.D18, board.num_pixels)
    pixels.brightness = 0.5

    # F Turns the NeoPixels red, green, and blue in sequence.
    def fade_red(self):
        self.pixels.fill((255, 0, 0))
        time.sleep(0.5)
        self.pixels.fill((0, 255, 0))
        time.sleep(0.5)
        self.pixels.fill((0, 0, 255))
        time.sleep(0.5)

    def random(self):
        red = 0x100000
        i = random.randint(0, self.pixel_nb)
        self.pixels[i] = red


