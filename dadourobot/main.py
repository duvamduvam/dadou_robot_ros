import logging.config
import sys

import board

from robot_config import I2C_ENABLED, SHUTDOWN_PIN, RESTART_PIN, STATUS_LED_PIN, STOP_KEY

#sys.path.append('..')

from dadou_utils.misc import Misc
from dadou_utils.utils.shutdown_restart import ShutDownRestart

from actions.neck import Neck
from robot_config import MAIN_DUE

from robot_factory import RobotFactory
from input.global_receiver import GlobalReceiver


print(sys.path)
print(dir(board))
print('Starting Didier')

shutdown_restart = ShutDownRestart(SHUTDOWN_PIN, RESTART_PIN, STATUS_LED_PIN)

audio = RobotFactory().get_audio()
face = RobotFactory().face
#lights = RobotFactory().lights
#lights = Lights(RobotFactory().get_strip())
neck = RobotFactory().neck
relays = RobotFactory().relays
wheel = RobotFactory().wheel
animations = RobotFactory().animation_manager

global_receiver = GlobalReceiver(RobotFactory().device_manager, animations)

while True:
    #logging.debug('run')

    try:
        msg = global_receiver.get_msg()

        if msg:
            audio.update(msg)
            neck.update(msg)
            face.update(msg)
            relays.update(msg)
            wheel.update(msg)
            #lights.update(msg)

        #if main_loop_sleep and main_loop_sleep != 0:
        #    time.sleep(main_loop_sleep)

        face.animate()
        #lights.animate()
        relays.process()
        wheel.check_stop(msg)
        #wheel.process()
        #neck.animate()
            #

        #if TimeUtils.is_time(SerialDeviceManager.last_update, SerialDeviceManager.update_period):
        #    RobotFactory().device_manager.update_devices()

        #wheel.test()

        shutdown_restart.process()

    except Exception as err:
        logging.error('exception {}'.format(err), exc_info=True)
