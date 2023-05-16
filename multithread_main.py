import logging.config
import subprocess
import sys

import cProfile
import time

import board
import neopixel
from dadou_utils.utils.shutdown_restart import ShutDownRestart
from dadou_utils.utils_static import SHUTDOWN_PIN, RESTART_PIN, STATUS_LED_PIN, LIGHTS_PIN, LIGHTS_LED_COUNT, \
    LOGGING_CONFIG_FILE, WHEELS, FACE, SERVOS, RANDOM, PROFILER, STOP, MAIN_THREAD, AUDIO
from dadou_utils.utils.time_utils import TimeUtils

from dadourobot.actions.audio_manager import AudioManager
from dadourobot.actions.face import Face
from dadourobot.actions.left_arm import LeftArm
from dadourobot.actions.neck import Neck
from dadourobot.actions.relays import RelaysManager
from dadourobot.actions.right_arm import RightArm
from dadourobot.actions.wheel import Wheel
from dadourobot.files.robot_json_manager import RobotJsonManager
from dadourobot.input.multithread_global_receiver import MultiGlobalReceiver
from dadourobot.robot_config import config
from dadourobot.sequences.animation_manager import AnimationManager

print(sys.path)
print(dir(board))
sys.path.append('')
sys.path.append('..')

print('Starting Didier')

if config[PROFILER]:
    profiler = cProfile.Profile()

print(config[LOGGING_CONFIG_FILE])
logging.config.fileConfig(config[LOGGING_CONFIG_FILE], disable_existing_loggers=False)

################################ Component initialisations ##################################
# TODO profiling
# TODO multitreading : https://makergram.com/community/topic/29/multi-thread-handling-for-normal-processes-using-python/4

components = []

robot_json_manager = RobotJsonManager(config)
pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False, brightness=0.05,
                           pixel_order=neopixel.GRB)

main_thread = (len(sys.argv) == 1)

if main_thread:
    logging.info("launch process")
    config[MAIN_THREAD] = True

    for param in [AUDIO, FACE, SERVOS, WHEELS]:
        logging.warning("lunch {} process".format(param))
        #process = subprocess.Popen(['sudo', 'python3', 'multithread_main.py', param], stdout=subprocess.PIPE)
    components.append(ShutDownRestart(config[SHUTDOWN_PIN], config[RESTART_PIN], config[STATUS_LED_PIN]))
else:
    logging.info("start {}".format(sys.argv[1]))

    if sys.argv[1] == AUDIO:
        components.append(AudioManager(config, robot_json_manager))
    elif sys.argv[1] == FACE:
        components.append(Face(config, robot_json_manager, pixels))
    elif sys.argv[1] == SERVOS:
        components.append(Neck(config))
        components.append(LeftArm(config))
        components.append(RightArm(config))
        components.append(RelaysManager(config, robot_json_manager))
    elif sys.argv[1] == WHEELS:
        components.append(ShutDownRestart(config[SHUTDOWN_PIN], config[RESTART_PIN], config[STATUS_LED_PIN]))
    #elif sys.argv[i] == LIGHTS:
    #    components.append(ShutDownRestart(config[SHUTDOWN_PIN], config[RESTART_PIN], config[STATUS_LED_PIN]))
    else:
        logging.error("wrong argument")

receiver = MultiGlobalReceiver(config, AnimationManager(config, robot_json_manager))

################################ Main loop ##################################

if config[PROFILER]:
    profiler.enable()

while True:

    try:
        msg = receiver.muli_get()

        if msg:

            #if STOP in msg and msg[STOP]:
            #    break

            for component in components:
                msg = component.update(msg)

        for component in components:
            component.process()

        #Reduce CPU load, better solution ?
        time.sleep(0.001)

    except Exception as err:
        logging.error('exception {}'.format(err), exc_info=True)

if config[PROFILER]:
    profiler.disable()
    profiler.dump_stats("profiler.stats")