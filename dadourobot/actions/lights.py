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
from dadou_utils.files.files_utils import FilesUtils
from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import METHOD, DEFAULT, DURATION, SEQUENCES, LOOP, COLOR, NAME, KEY, KEYS, LIGHTS
from microcontroller import Pin
from rpi_ws281x import Adafruit_NeoPixel

from dadourobot.actions.sequence import Sequence
from dadourobot.robot_static import JSON_LIGHTS
from dadourobot.visual.lights_animations import LightsAnimations


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
    LED_COUNT = 782 # Number of LED pixels.
    FIRST_STRIP_LED = 513

    # TODO check examples : https://www.digikey.fr/en/maker/projects/circuitpython-led-animations/d15c769c6f6d411297657c35f0166958

    sequences_key = {}
    sequences_name = {}

    sequence = {}
    current_animation = {}
    animations = {}


    def __init__(self, config, json_manager, strip):
        self.config = config
        #self.strip = neopixel.NeoPixel(self.LED_COUNT, Pin(config.LIGHTS_PIN), self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)

        strip_pixels_range = ()
        for x in range(self.FIRST_STRIP_LED, self.LED_COUNT): #513
            strip_pixels_range += (x,)

        self.strip = PixelMap(strip,
            strip_pixels_range, individual_pixels=True)

        self.animations = LightsAnimations(self.LED_COUNT - self.FIRST_STRIP_LED, self.strip)
        self.json_manager = json_manager
        self.load_sequences()
        self.update({KEY:DEFAULT})

    def load_sequences(self):
        lights_sequences = self.json_manager.open_json(JSON_LIGHTS)
        for seq in lights_sequences:
            for key in seq[KEYS]:
                self.sequences_key[key] = seq
            self.sequences_name[seq[NAME]] = seq

    def update(self, msg):

        json_seq = self.get_lights_sequence(msg)
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

    def get_lights_sequence(self, msg):
        if msg and KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if msg and LIGHTS in msg and msg[LIGHTS] in self.sequences_name.keys():
            return self.sequences_name[msg[LIGHTS]]

    def animate(self):
        if not self.sequence.loop and TimeUtils.is_time(self.sequence.start_time, self.sequence.duration):
            self.update({KEY:DEFAULT})
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
