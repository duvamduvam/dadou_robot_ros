import logging.config
import sys

import board
import neopixel

from dadou_utils.com.serial_devices_manager import SerialDeviceManager
from dadou_utils.utils.shutdown_restart import ShutDownRestart
from dadou_utils.utils_static import SHUTDOWN_PIN, RESTART_PIN, STATUS_LED_PIN, DEVICES_LIST, LIGHTS_PIN, LIGHTS, \
    LIGHTS_LED_COUNT, LOGGING_CONFIG_FILE

from dadourobot.sequences.animation_manager import AnimationManager
from dadourobot.actions.neck import Neck
from dadourobot.actions.audio_manager import AudioManager
from dadourobot.actions.face import Face
from dadourobot.actions.left_arm import LeftArm
from dadourobot.actions.lights import Lights
from dadourobot.actions.relays import RelaysManager
from dadourobot.actions.right_arm import RightArm
from dadourobot.actions.wheel import Wheel
from dadourobot.files.robot_json_manager import RobotJsonManager
from dadourobot.input.global_receiver import GlobalReceiver
from dadourobot.robot_config import config

print(sys.path)
print(dir(board))
sys.path.append('')
sys.path.append('..')

print('Starting Didier')

print(config[LOGGING_CONFIG_FILE])
logging.config.fileConfig(config[LOGGING_CONFIG_FILE], disable_existing_loggers=False)

################################ Component initialisations ##################################
# TODO profiling
# TODO multitreading : https://makergram.com/community/topic/29/multi-thread-handling-for-normal-processes-using-python/4

components = []

robot_json_manager = RobotJsonManager(config)
pixels = neopixel.NeoPixel(config[LIGHTS_PIN], config[LIGHTS_LED_COUNT], auto_write=False, brightness=0.05, pixel_order=neopixel.GRB)

#TODO check best order for performances
components.extend([AudioManager(config, robot_json_manager),
                    Face(config, robot_json_manager, pixels),
                    LeftArm(config),
                    #Lights(config, robot_json_manager, pixels, LIGHTS),
                    Neck(config),
                    RelaysManager(config, robot_json_manager),
                    RightArm(config),
                    ShutDownRestart(config[SHUTDOWN_PIN], config[RESTART_PIN], config[STATUS_LED_PIN]),
                    Wheel(config),
                   ])

#devices_manager = SerialDeviceManager(DEVICES_LIST)
animations = AnimationManager(config, robot_json_manager)
global_receiver = GlobalReceiver()

################################ Main loop ##################################

while True:
    # logging.debug('run')

    try:
        msg = global_receiver.get_msg()

        if msg:
            for component in components:
                component.update(msg)

        for component in components:
            component.process()

        #wheel.check_stop(msg)


    except Exception as err:
        logging.error('exception {}'.format(err), exc_info=True)
