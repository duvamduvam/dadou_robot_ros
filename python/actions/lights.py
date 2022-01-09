# linux rpi install : sudo pip3 install Adafruit-Blinka
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka
# sudo pip3 install adafruit-circuitpython-led-animation

import neopixel
import logging.config

# todo check thread : https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
# todo check thread2 : https://riptutorial.com/python/example/4691/communicating-between-threads
from microcontroller import Pin

from python.visual.animations import Animations
from python.config import Config
from python.json_manager import JsonManager
from python.sequence import Sequence
from python.utils import Utils


class Lights:
    # LED strip configuration:
    LED_COUNT = 64 * 6  # Number of LED pixels.
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

    def __init__(self, json_manager: JsonManager, config: Config):
        self.strip = neopixel.NeoPixel(Pin(config.LIGHTS_PIN), self.LED_COUNT)
        self.strip.brightness = 0.1
        self.animations = Animations(self.LED_COUNT, self.strip)
        self.json_manager = json_manager
        self.update('default')

    def update(self, key):
        json_seq = self.json_manager.get_lights(key)
        if not json_seq:
            return
        sequences = []
        for s in json_seq[JsonManager.SEQUENCE]:
            animation = Animation(s[JsonManager.METHOD], s[JsonManager.DURATION])
            color_name = self.json_manager.get_attribut(s, JsonManager.COLOR)
            if color_name:
                animation.color = self.json_manager.get_color(color_name)
            sequences.append(animation)
        self.sequence = Sequence(json_seq[JsonManager.DURATION], json_seq[JsonManager.LOOP], sequences)

        self.current_animation = getattr(self.animations, self.sequence.current_element.method)(
            self.sequence.current_element)
        logging.info("update lights sequence to " + json_seq[JsonManager.NAME])

    def animate(self):
        if not self.sequence.loop and Utils.is_time(self.sequence.start_time, self.sequence.duration):
            self.update('default')
            return

        if Utils.is_time(self.sequence.current_element.start_time, self.sequence.current_element.timeout):
            self.sequence.next()
            self.current_animation = getattr(self.animations, self.sequence.current_element.method)(
                self.sequence.current_element)
            #logging.debug(
            #    "change sequence to " + self.sequence.current_element.method + " with time " + str(
            #        self.sequence.current_element.timeout))
        self.current_animation.animate()


class Animation:
    color = ()
    timeout = 0
    start_time = Utils.current_milli_time()

    def __init__(self, method, timeout: int):
        logging.debug("add animation method : " + method + " timeout : " + str(timeout))
        self.method = method
        self.timeout = timeout

    def set_color(self, color):
        self.color = color
