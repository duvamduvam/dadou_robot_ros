# linux rpi install : sudo pip3 install Adafruit-Blinka
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka
# sudo pip3 install adafruit-circuitpython-led-animation

import logging.config

# todo check thread : https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
# todo check thread2 : https://riptutorial.com/python/example/4691/communicating-between-threads
from adafruit_led_animation.helper import PixelMap
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import METHOD, DEFAULT, DURATION, SEQUENCES, LOOP, COLOR, NAME, KEY, LIGHTS, FACE

from dadourobot.actions.abstract_actions import ActionsAbstract
from dadourobot.sequences.sequence import Sequence
from dadourobot.robot_config import JSON_LIGHTS
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


class Lights(ActionsAbstract):
    # LED strip configuration:
    LED_COUNT = 782 # Number of LED pixels.
    FIRST_STRIP_LED = 513

    # TODO check examples : https://www.digikey.fr/en/maker/projects/circuitpython-led-animations/d15c769c6f6d411297657c35f0166958

    sequences_key = {}
    sequences_name = {}

    sequence = {}
    current_animation = {}
    animations = {}

    duration = 0
    start_time = 0

    def __init__(self, json_manager, strip):
        super().__init__(json_manager, JSON_LIGHTS)
        #self.strip = neopixel.NeoPixel(self.LED_COUNT, Pin(config.LIGHTS_PIN), self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)

        strip_pixels_range = ()
        for x in range(self.FIRST_STRIP_LED, self.LED_COUNT): #513
            strip_pixels_range += (x,)

        self.strip = PixelMap(strip,
            strip_pixels_range, individual_pixels=True)

        self.animations = LightsAnimations(self.LED_COUNT - self.FIRST_STRIP_LED, self.strip)
        self.update({LIGHTS:DEFAULT})

    def update(self, msg):

        json_seq = self.get_sequence(msg, LIGHTS, True)
        if not json_seq:
            return

        self.duration = json_seq[DURATION]
        self.loop = json_seq[LOOP]
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
        #self.sequence.start_time = TimeUtils.current_milli_time()
        self.start_time = TimeUtils.current_milli_time()
        logging.info("update lights sequences to " + json_seq[NAME])

    def animate(self):

        if self.loop_duration != 0:
            if TimeUtils.is_time(self.start_loop_duration, self.loop_duration):
                self.loop_duration = 0
                self.loop = False

        if not self.loop and TimeUtils.is_time(self.start_time, self.duration):
            self.update({LIGHTS:DEFAULT})
            return

        if self.sequence.time_to_switch():
            self.sequence.next()
            self.sequence.current_element.start_time = TimeUtils.current_milli_time()
            self.current_animation = getattr(self.animations, self.sequence.current_element.method)(
                self.sequence.current_element)
            self.sequence.current_element.start_time = TimeUtils.current_milli_time()
            # logging.debug(
            #    "change sequences to " + self.sequences.current_element.method + " with time " + str(
            #        self.sequences.current_element.duration))
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
