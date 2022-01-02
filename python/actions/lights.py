# linux rpi install : sudo pip3 install Adafruit-Blinka
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka
# sudo pip3 install adafruit-circuitpython-led-animation
import random
import time
import board
import neopixel
import logging.config
from rainbowio import colorwheel
from adafruit_led_animation import helper
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.color import \
    AMBER, BLACK, BLUE, CYAN, GREEN, JADE, ORANGE, PURPLE, RED, MAGENTA, TEAL, WHITE, YELLOW

# todo check thread : https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
# todo check thread2 : https://riptutorial.com/python/example/4691/communicating-between-threads
from python.json_manager import JsonManager


class Lights:
    # LED strip configuration:
    LED_COUNT = 64 * 6  # Number of LED pixels.
    LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 0  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

    strip = neopixel.NeoPixel(board.D18, LED_COUNT)
    strip.brightness = 0.1

    pixel_wing_vertical = helper.PixelMap.vertical_lines(
        strip, 8 * 6, 8, helper.horizontal_strip_gridmap(8, alternating=False)
    )
    pixel_wing_horizontal = helper.PixelMap.horizontal_lines(
        strip, 8, 4, helper.horizontal_strip_gridmap(24, alternating=False)
    )

    # strip = neopixel.NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    # strip.begin()

    # F Turns the NeoPixels red, green, and blue in sequence.
    # TODO check examples : https://www.digikey.fr/en/maker/projects/circuitpython-led-animations/d15c769c6f6d411297657c35f0166958

    current_animation = {}

    def __init__(self, json_manager: JsonManager):
        self.default()
        self.json_manager = json_manager

    def update(self, key):
        json_light = self.json_manager.get_lights(key)
        if 'color' in json_light:
            logging.debug(
                "update lights with key : {key} method : {json_light['method']}, color : {json_light['color']}")
            json_color = json_light['color']
            color = self.json_manager.get_color(key)
            getattr(self, json_light['method'])(json_light, color)

        else:
            getattr(self, json_light['method'])(json_light)

    def default(self):
        self.current_animation = Chase(self.strip, speed=0.1, color=RED, size=3, spacing=6)

    def chase(self, parameters, color):
        self.current_animation = Chase(self.strip, speed=0.1, color=color, size=3, spacing=6)

    def blink(self, parameters, color):
        self.current_animation = Blink(self.strip, speed=0.5, color=color)

    def color_cycle(self, parameters):
        self.current_animation = ColorCycle(self.strip, 0.5, colors=[MAGENTA, ORANGE, TEAL])

    def comet(self, parameters):
        self.current_animation = Rainbow(self.pixel_wing_vertical, speed=0.1, period=2)

    def pulse(self, parameters):
        self.current_animation = Pulse(self.strip, speed=0.1, color=AMBER, period=3)

    def rainbow(self, parameters):
        self.current_animation = Rainbow(self.strip, speed=0.1, period=2)

    def rainbow_chase(self, parameters):
        self.current_animation = RainbowChase(self.strip, speed=0.1, size=5, spacing=3)

    def rainbow_comet(self, parameters):
        self.current_animation = RainbowComet(self.strip, speed=0.1, tail_length=7, bounce=True)

    def rainbow_sparkle(self, parameters):
        self.current_animation = RainbowSparkle(self.strip, speed=0.1, num_sparkles=15)

    def sparkle(self, parameters):
        self.current_animation = Sparkle(self.strip, speed=0.05, color=AMBER, num_sparkles=10)

    def sparkle_pulse(self, parameters):
        self.current_animation = SparklePulse(self.strip, speed=0.05, period=3, color=JADE)

    def fade_red(self):
        self.strip.fill((255, 0, 0))
        time.sleep(0.5)
        self.strip.fill((0, 255, 0))
        time.sleep(0.5)
        self.strip.fill((0, 0, 255))
        time.sleep(0.5)

    def random(self):
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
        time.sleep(0.5)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.LED_COUNT):
                rc_index = (i * 256 // self.LED_COUNT) + j
                self.strip[i] = colorwheel(rc_index & 255)
            self.strip.show()
            time.sleep(wait)

    def animate(self):
        self.current_animation.animate()

    # def animate_loop(self, time):
    # todo animate with time
    #    self.current_animation.animate()
