# linux rpi install : sudo pip3 install Adafruit-Blinka
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka
# sudo pip3 install adafruit-circuitpython-led-animation

import neopixel
import logging.config

# todo check thread : https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
# todo check thread2 : https://riptutorial.com/python/example/4691/communicating-between-threads
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, WHITE, BLACK, GOLD, PINK, AQUA, JADE, AMBER
from adafruit_led_animation.helper import PixelMap
from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import METHOD, DURATION, SEQUENCES, LOOP, COLOR, NAME, KEY
from microcontroller import Pin
from rpi_ws281x import Adafruit_NeoPixel

from dadourobot.actions.sequence import Sequence
from dadourobot.visual.animations import Animations
from dadourobot.utils import Utils

"""
      "method": "sparkle_pulse",
      "color": "AMBER"
      "method": "chase",
      "color": "RED"
      "method": "blink",
      "color": "BLUE"
      "method": "color_cycle"
      "method": "pulse",
      "color": "BLUE"
      "method": "rainbow_chase"
      "method": "rainbow_comet"
      "method": "color_cycle"
      "method": "comet"
"""


class Lights:
    # LED strip configuration:
    LED_COUNT = 100 # Number of LED pixels.
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 0  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

    strip = {}

    """
    pixel_wing_vertical = helper.PixelMap.vertical_lines(
        strip, 8 * 6, 8, helper.horizontal_strip_gridmap(8, alternating=False)
    )
    pixel_wing_horizontal = helper.PixelMap.horizontal_lines(
        strip, 8, 4, helper.horizontal_strip_gridmap(24, alternating=False)
    )
    """

    # strip = neopixel.NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    # strip.begin()

    # F Turns the NeoPixels red, green, and blue in sequence.
    # TODO check examples : https://www.digikey.fr/en/maker/projects/circuitpython-led-animations/d15c769c6f6d411297657c35f0166958

    sequence = {}
    current_animation = {}
    animations = {}

    """LED_COUNT = 40
    LED_PIN = 13
    # LED_PIN        = 10     
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 255
    LED_INVERT = False
    LED_CHANNEL = 0
    #https://forums.raspberrypi.com/viewtopic.php?t=274479
    """

    def __init__(self, config, json_manager, strip):
        self.config = config
        #self.strip = neopixel.NeoPixel(self.LED_COUNT, Pin(config.LIGHTS_PIN), self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)

        strip_pixels_range = ()
        for x in range(513, 713): #513
            strip_pixels_range += (x,)

        self.strip = PixelMap(strip,
            strip_pixels_range, individual_pixels=True)
        #self.strip = strip

        #self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 1)

        self.animations = Animations(self.LED_COUNT, self.strip)
        self.json_manager = json_manager
        self.update({KEY:'default'})

    def update(self, msg):
        if msg and KEY in msg:
            json_seq = self.json_manager.get_lights(msg[KEY])
            if not json_seq:
                return
            sequences = []
            for s in json_seq[SEQUENCES]:
                animation = [s[DURATION], Animation(s[METHOD], s[DURATION])]
                color_name = self.json_manager.get_attribut(s, COLOR)
                if color_name:
                    animation[1].color = self.json_manager.get_color(color_name)
                sequences.append(animation)
            self.sequence = Sequence(json_seq[DURATION], json_seq[LOOP], sequences, 0)

            #self.current_animation = Comet(self.strip, speed=0.01, color=PURPLE, tail_length=50, bounce=True)

            #TODO animation parameters not working
            self.current_animation = getattr(self.animations, self.sequence.current_element.method)(
                self.sequence.current_element)
            self.sequence.start_time = TimeUtils.current_milli_time()
            logging.info("update lights sequence to " + json_seq[NAME])

    def animate(self):
        if not self.sequence.loop and TimeUtils.is_time(self.sequence.start_time, self.sequence.duration):
            self.update('default')
            return

        if self.sequence.time_to_switch():
            self.sequence.next()
            self.sequence.current_element.start_time = TimeUtils.current_milli_time()
            self.current_animation = getattr(self.animations, self.sequence.current_element.method)(
                self.sequence.current_element)
            self.sequence.current_element.start_time = TimeUtils.current_milli_time()
            # logging.debug(
            #    "change sequence to " + self.sequence.current_element.method + " with time " + str(
            #        self.sequence.current_element.duration))
        self.current_animation.animate()


class Animation:
    color = ()
    duration = 0
    start_time = TimeUtils.current_milli_time()

    def __init__(self, method, duration: int):
        logging.debug("add animation method : " + method + " duration : " + str(duration))
        self.method = method
        self.duration = duration

    def set_color(self, color):
        self.color = color
