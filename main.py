
import cProfile
import logging.config
import subprocess
import sys
import time

import board
import neopixel
from adafruit_led_animation.helper import PixelMap, PixelSubset

from dadou_utils.logging_conf import LoggingConf
from dadou_utils.utils.status import Status
from dadou_utils.utils_static import ANIMATION, LIGHTS, SHUTDOWN_PIN, RESTART_PIN, STATUS_LED_PIN, LIGHTS_PIN, \
    LIGHTS_LED_COUNT, \
    LOGGING_CONFIG_FILE, WHEELS, FACE, SERVOS, PROFILER, MAIN_THREAD, AUDIO, TYPE, TYPES, NECK, LEFT_ARM, RIGHT_ARM, \
    SINGLE_THREAD, LOGGING_FILE_NAME, MULTI_THREAD, PROCESS_NAME, LEFT_EYE, RIGHT_EYE, HEAD_PWM_NB, \
    LEFT_EYE_NB, RIGHT_EYE_NB, LEFT_ARM_NB, RIGHT_ARM_NB, I2C_ENABLED, PWM_CHANNELS_ENABLED, ROBOT, JSON_LIGHTS, \
    LIGHTS_START_LED, LIGHTS_END_LED
from dadourobot.actions.audio_manager import AudioManager
from dadourobot.actions.face import Face
from dadourobot.actions.lights import Lights
from dadourobot.actions.relays import RelaysManager
from dadourobot.actions.servo import Servo
from dadourobot.actions.wheel import Wheel
from dadourobot.files.robot_json_manager import RobotJsonManager
from dadourobot.input.global_receiver import GlobalReceiver
from dadourobot.robot_config import config
from dadourobot.sequences.animation_manager import AnimationManager

#print(sys.path)
#print(dir(board))
sys.path.append('')
sys.path.append('..')

config[MAIN_THREAD] = (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] == SINGLE_THREAD)
config[MULTI_THREAD] = True

if config[PROFILER]:
    profiler = cProfile.Profile()

#print(config[LOGGING_CONFIG_FILE])
#logging.config.fileConfig(config[LOGGING_CONFIG_FILE], disable_existing_loggers=False)
if len(sys.argv) > 1:
    process_name = sys.argv[1]
else:
    process_name = 'main'
logging.config.dictConfig(LoggingConf.get(config[LOGGING_FILE_NAME], process_name))

################################ Component initialisations ##################################
# TODO profiling
# TODO multitreading : https://makergram.com/community/topic/29/multi-thread-handling-for-normal-processes-using-python/4

components = []

robot_json_manager = RobotJsonManager(config)
pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False, brightness=0.05)

strip_pixels_range = ()
for x in range(0, 512):
    strip_pixels_range += (x,)

face_strip = PixelSubset(pixels, 0, config[LIGHTS_START_LED] - 1)
#face_strip = PixelMap(pixels, strip_pixels_range, individual_pixels=True)

config[TYPES] = [ANIMATION, AUDIO, FACE, LIGHTS, NECK, LEFT_ARM, RIGHT_ARM]
receiver = GlobalReceiver(config, AnimationManager(config, robot_json_manager))

input_components = []

if len(sys.argv) > 1:
    config[PROCESS_NAME] = sys.argv[1]
else:
    config[PROCESS_NAME] = "main"

if config[MAIN_THREAD]:
    logging.info("start main thread")
    config[MAIN_THREAD] = True

    if not (len(sys.argv) > 1 and sys.argv[1] == SINGLE_THREAD):
        for param in [AUDIO, FACE, LIGHTS, SERVOS, WHEELS]:
            logging.warning("lunch {} process".format(param))
            # stdout=subprocess.PIPE, stderr=subprocess.PIPE because it stopped the process after a certain amount of log
            subprocess.Popen(['python3', 'main.py', param])
    else:
        input_components.extend([AUDIO, LIGHTS, SERVOS, WHEELS])
    components.extend([Status(config[SHUTDOWN_PIN], config[STATUS_LED_PIN], config[RESTART_PIN])])
    components.append(AudioManager(config, receiver, robot_json_manager))
else:
    input_components.append(sys.argv[1])

for component in input_components:
    logging.info("start {}".format(component))
    config[TYPE] = sys.argv[1]
    if component == AUDIO:
        pass
        #components.append(AudioManager(config, receiver, robot_json_manager))
    elif component == LIGHTS:
        #Face matrix and lights strip component can't be in separate process, otherwise strange behaviour appear
        components.append(Face(config, receiver, robot_json_manager, face_strip))
        components.append(Lights(config=config, start=config[LIGHTS_START_LED], end=config[LIGHTS_END_LED],
                                 json_manager=robot_json_manager, global_strip=pixels, light_type='robot_lights', json_light=config[JSON_LIGHTS]))
    elif component == SERVOS:
        components.append(Servo(NECK, config[HEAD_PWM_NB], 50, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        components.append(Servo(LEFT_EYE, config[LEFT_EYE_NB], 55, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        components.append(Servo(RIGHT_EYE, config[RIGHT_EYE_NB], 55, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        components.append(Servo(LEFT_ARM, config[LEFT_ARM_NB], 99, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        components.append(Servo(RIGHT_ARM, config[RIGHT_ARM_NB], 99, 180, config[I2C_ENABLED], config[PWM_CHANNELS_ENABLED], receiver))
        components.append(RelaysManager(config, receiver, robot_json_manager))
    #elif component == LIGHTS:
    #    #config, start, end, json_manager, global_strip, light_type
    #    #TODO check led number
    #    components.append(Lights(config=config, start=config[LIGHTS_START_LED], end=config[LIGHTS_END_LED],
    #                             json_manager=robot_json_manager, global_strip=pixels, light_type='ROBOT_LIGHTS', json_light=config[JSON_LIGHTS]))
    elif component == WHEELS:
        components.append(Wheel(config, receiver))
    else:
        logging.error("wrong argument")




################################ Main loop ##################################

while True:

    try:
        msg = receiver.multi_get()
        if msg:
            for component in components:
                msg = component.update(msg)

        for component in components:
            component.process()

        #Reduce CPU load, better solution ?
        time.sleep(0.001)

    except Exception as err:
        logging.error('exception {}'.format(err), exc_info=True)
