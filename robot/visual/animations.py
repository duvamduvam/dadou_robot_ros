import logging
import random
import time

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.color import \
    BLACK, ORANGE, MAGENTA, TEAL
from rainbowio import colorwheel


class Animations:

    def __init__(self, led_count, strip):
        self.LED_COUNT = led_count
        self.strip = strip

    def default(self, params):
        return Chase(self.strip, speed=0.1, color=params.color, size=3, spacing=6)

    def chase(self, params):
        return Chase(self.strip, speed=0.1, color=params.color, size=3, spacing=6)

    def blink(self, params):
        return Blink(self.strip, speed=0.5, color=params.color)

    def color_cycle(self, params):
        return ColorCycle(self.strip, 0.5, colors=[MAGENTA, ORANGE, TEAL])

    def comet(self, params):
        return Rainbow(self.strip, speed=0.1, period=2)

    def pulse(self, params):
        return Pulse(self.strip, speed=0.1, color=params.color, period=3)

    def rainbow(self, params):
        return Rainbow(self.strip, speed=0.1, period=2)

    def rainbow_chase(self, params):
        return RainbowChase(self.strip, speed=0.1, size=5, spacing=3)

    def rainbow_comet(self, params):
        return RainbowComet(self.strip, speed=0.1, tail_length=7, bounce=True)

    def rainbow_sparkle(self, params):
        return RainbowSparkle(self.strip, speed=0.1, num_sparkles=15)

    def sparkle(self, params):
        return Sparkle(self.strip, speed=0.05, color=params.color, num_sparkles=10)

    def sparkle_pulse(self, params):
        return SparklePulse(self.strip, speed=0.05, period=3, color=params.color)

    def fade_red(self, params):
        self.strip.fill((255, 0, 0))
        time.sleep(0.5)
        self.strip.fill((0, 255, 0))
        time.sleep(0.5)
        self.strip.fill((0, 0, 255))
        time.sleep(0.5)

    def random(self, params):
        # red = 0x100000
        i = random.randint(0, self.LED_COUNT - 1)

        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        logging.debug("random strip[" + str(i) + "] blue " + str(blue) + " red " + str(red) + " green " + str(green))
        self.strip[i] = (red, green, blue)
        self.strip.show()

    def fill(self, color):
        logging.info("fill strip with " + str(color))
        self.strip.fill(color)

    def clean(self):
        self.strip.fill(BLACK)

    def color_chase(self, color, wait):
        for i in range(self.LED_COUNT):
            self.strip[i] = color
            time.sleep(wait)
            self.strip.show()
            # todo delete time.sleep
        time.sleep(0.5)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.LED_COUNT):
                rc_index = (i * 256 // self.LED_COUNT) + j
                self.strip[i] = colorwheel(rc_index & 255)
            self.strip.show()
            # todo delete time.sleep
            time.sleep(wait)
