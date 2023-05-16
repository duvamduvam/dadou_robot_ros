
import cProfile
import logging.config
import subprocess
import sys
import time

import board
import neopixel

from dadou_utils.logging_conf import LoggingConf
from dadou_utils.utils.shutdown_restart import ShutDownRestart
from dadou_utils.utils_static import ANIMATION, LIGHTS, SHUTDOWN_PIN, RESTART_PIN, STATUS_LED_PIN, LIGHTS_PIN, \
    LIGHTS_LED_COUNT, \
    LOGGING_CONFIG_FILE, WHEELS, FACE, SERVOS, PROFILER, MAIN_THREAD, AUDIO, TYPE, TYPES, NECK, LEFT_ARM, RIGHT_ARM, \
    SINGLE_THREAD, LOGGING, PROCESS, LOGGING_FILE_NAME, MULTI_THREAD, PROCESS_NAME
from dadourobot.actions.audio_manager import AudioManager
from dadourobot.actions.face import Face
from dadourobot.actions.left_arm import LeftArm
from dadourobot.actions.left_eye import LeftEye
from dadourobot.actions.neck import Neck
from dadourobot.actions.relays import RelaysManager
from dadourobot.actions.right_arm import RightArm
from dadourobot.actions.right_eye import RightEye
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
pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False, brightness=0.05,
                           pixel_order=neopixel.GRB)

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
        for param in [AUDIO, FACE, SERVOS, WHEELS]:
            logging.warning("lunch {} process".format(param))
            # stdout=subprocess.PIPE, stderr=subprocess.PIPE because it stopped the process after a certain amount of log
            subprocess.Popen(['python3', 'main.py', param])
    else:
        input_components.extend([AUDIO, FACE, SERVOS, WHEELS])
    components.extend([ShutDownRestart(config[SHUTDOWN_PIN], config[STATUS_LED_PIN], config[RESTART_PIN])])
else:
    input_components.append(sys.argv[1])

for component in input_components:
    logging.info("start {}".format(component))
    config[TYPE] = sys.argv[1]
    if component == AUDIO:
        components.append(AudioManager(config, receiver, robot_json_manager))
    elif component == FACE:
        components.append(Face(config, receiver, robot_json_manager, pixels))
    elif component == SERVOS:
        components.append(Neck(config, receiver))
        components.append(LeftArm(config, receiver))
        components.append(RightArm(config, receiver))
        components.append(LeftEye(config, receiver))
        components.append(RightEye(config, receiver))
        components.append(RelaysManager(config, receiver, robot_json_manager))
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
