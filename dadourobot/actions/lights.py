    # linux rpi install : sudo pip3 install Adafruit-Blinka
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka
# sudo pip3 install adafruit-circuitpython-led-animation

import logging.config

    # todo check thread : https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
# todo check thread2 : https://riptutorial.com/python/example/4691/communicating-between-threads
import logging.config

import adafruit_led_animation.color as color
    # todo check thread : https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
    # todo check thread2 : https://riptutorial.com/python/example/4691/communicating-between-threads
from adafruit_led_animation.helper import PixelSubset

from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import METHOD, DEFAULT, DURATION, SEQUENCES, LOOP, COLOR, NAME, JSON_COLORS, \
    JSON_LIGHTS_BASE, BRIGHTNESS
from dadourobot.actions.abstract_json_actions import AbstractJsonActions
from dadourobot.sequences.sequence import Sequence
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


class Lights(AbstractJsonActions):
    # LED strip configuration:
    LED_COUNT = 782 # Number of LED pixels.
    FIRST_STRIP_LED = 513

    # TODO check examples : https://www.digikey.fr/en/maker/projects/circuitpython-led-animations/d15c769c6f6d411297657c35f0166958

    sequence = {}
    current_animation = {}
    animations_methods = {}
    default = DEFAULT
    duration = 0
    start_time = 0

    def __init__(self, config, start, end, json_manager, global_strip, light_type, json_light):
        self.light_type = light_type
        super().__init__(config=config, json_manager=json_manager, action_type=self.light_type, json_file=json_light)

        self.strip = PixelSubset(global_strip, start, end)
        #self.strip.brightness = 1
        #self.strip = global_strip
        self.colors = json_manager.get_json_file(config[JSON_COLORS])
        self.lights_base = self.load_light_base(config, json_manager)
        self.animations_methods = LightsAnimations(end - start, self.strip)
        self.update({light_type: DEFAULT})

    def load_light_base(self, config, json_manager):
        lights_base = json_manager.get_json_file(config[JSON_LIGHTS_BASE])
        for light_name in lights_base:
            if COLOR in lights_base[light_name]:
                lights_base[light_name][COLOR] = self.get_color(lights_base[light_name][COLOR])

        return lights_base

    def update(self, msg):

        if BRIGHTNESS in msg:
            logging.info("update brightness to {}".format(msg[BRIGHTNESS]))
            self.strip.brightness = float(msg[BRIGHTNESS])

        json_seq = self.get_sequence(msg, True)
        if not json_seq:
            return

        if DURATION in msg:
            self.duration = msg[DURATION]
        else:
            self.duration = json_seq[DURATION]
        self.loop = json_seq[LOOP]

        if DEFAULT in json_seq:
            self.default = json_seq[NAME]

        sequences = []
        for lights_base, duration in json_seq[SEQUENCES].items():
            animation = [duration, LightAnimation(lights_base, duration)]
            #color_name = self.json_manager.get_attribut(s, COLOR)
            if COLOR in animation and COLOR in self.colors:
                #TODO pourquoi animation 1 ?
                animation[1].color = self.colors[animation[COLOR]]
            sequences.append(animation)
        self.sequence = Sequence(json_seq[DURATION], json_seq[LOOP], sequences, 0)

        #TODO animation parameters not working
        #Initiate light method
        self.load_light_method(self.sequence.current_element.method)

        #self.sequence.start_time = TimeUtils.current_milli_time()
        self.start_time = TimeUtils.current_milli_time()
        logging.info("update lights {} sequences to {}".format(self.light_type, json_seq[NAME]))

    def load_light_method(self, light_name):

        if light_name not in self.lights_base:
            logging.error("{} not in lights base".format(light_name))
            return
        light = self.lights_base[light_name]
        if not hasattr(self.animations_methods, light[METHOD]):
            logging.error('{} not in lights base'.format(light[METHOD]))
            return
        self.current_animation = getattr(self.animations_methods, light[METHOD])(
            light)

    def get_color(self, color_name):
        if color_name in self.colors:
            return self.colors[color_name][0], self.colors[color_name][1], self.colors[color_name][2]
        else:
            logging.error("color {} not defined".format(color))

    def process(self):
        if not self.loop and TimeUtils.is_time(self.start_time, self.duration):
            self.update({self.light_type: self.default})

        if self.sequence.time_to_switch():
            self.sequence.next()
            #self.sequence.current_element.start_time = TimeUtils.current_milli_time()
            self.load_light_method(self.sequence.current_element.method)
            #self.sequence.current_element.start_time = TimeUtils.current_milli_time()"""

        self.current_animation.animate()


class LightAnimation:
    color = ()
    duration = 0
    start_time = TimeUtils.current_milli_time()

    def __init__(self, method, duration: int):
        logging.debug("add animation method : " + method + " duration : " + str(duration))
        self.method = method
        self.duration = duration

    def set_color(self, color):
        self.color = color
