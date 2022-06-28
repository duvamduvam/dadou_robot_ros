# linux rpi install : sudo pip3 install Adafruit-Blinka
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka
# sudo pip3 install adafruit-circuitpython-led-animation

import neopixel
import logging.config

# todo check thread : https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
# todo check thread2 : https://riptutorial.com/python/example/4691/communicating-between-threads
from microcontroller import Pin
from rpi_ws281x import Adafruit_NeoPixel

from dadourobot.robot_factory import RobotFactory
from dadourobot.robot_static import RobotStatic
from dadourobot.visual.animations import Animations
from dadourobot.sequence import Sequence
from dadourobot.utils import Utils


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

    def __init__(self, strip):
        config = RobotFactory().config
        #self.strip = neopixel.NeoPixel(self.LED_COUNT, Pin(config.LIGHTS_PIN), self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip = strip

        #self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, 1)

        self.animations = Animations(self.LED_COUNT, self.strip)
        self.json_manager = RobotFactory().robot_json_manager
        self.update('default')

    def update(self, key):
        if key:
            json_seq = self.json_manager.get_lights(key)
            if not json_seq:
                return
            sequences = []
            for s in json_seq[RobotStatic.SEQUENCE]:
                animation = Animation(s[RobotStatic.METHOD], s[RobotStatic.DURATION])
                color_name = self.json_manager.get_attribut(s, RobotStatic.COLOR)
                if color_name:
                    animation.color = self.json_manager.get_color(color_name)
                sequences.append(animation)
            self.sequence = Sequence(json_seq[RobotStatic.DURATION], json_seq[RobotStatic.LOOP], sequences)

            self.current_animation = getattr(self.animations, self.sequence.current_element.method)(
                self.sequence.current_element)
            self.sequence.start_time = Utils.current_milli_time()
            logging.info("update lights sequence to " + json_seq[RobotStatic.NAME])

    def animate(self):
        if not self.sequence.loop and Utils.is_time(self.sequence.start_time, self.sequence.duration):
            self.update('default')
            return

        if Utils.is_time(self.sequence.current_element.start_time, self.sequence.current_element.duration):
            self.sequence.next()
            self.sequence.current_element.start_time = Utils.current_milli_time()
            self.current_animation = getattr(self.animations, self.sequence.current_element.method)(
                self.sequence.current_element)
            self.sequence.current_element.start_time = Utils.current_milli_time()
            # logging.debug(
            #    "change sequence to " + self.sequence.current_element.method + " with time " + str(
            #        self.sequence.current_element.duration))
        self.current_animation.animate()


class Animation:
    color = ()
    duration = 0
    start_time = Utils.current_milli_time()

    def __init__(self, method, duration: int):
        logging.debug("add animation method : " + method + " duration : " + str(duration))
        self.method = method
        self.duration = duration

    def set_color(self, color):
        self.color = color
