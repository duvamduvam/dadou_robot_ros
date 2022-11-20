import logging.config
import sys
import traceback

import board
import digitalio
from dadou_utils.com.serial_devices_manager import SerialDeviceManager
from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import WHEEL_LEFT, WHEEL_RIGHT
from digitalio import DigitalInOut, Direction

import time

#sys.path.append('..')

from dadou_utils.misc import Misc

from dadourobot.actions.neck import Neck
from dadourobot.com.main_due_com import MainDueCom
from dadourobot.robot_static import MAIN_DUE

from dadourobot.robot_factory import RobotFactory
from dadourobot.input.global_receiver import GlobalReceiver


print(sys.path)
print('Starting didier')



audio = RobotFactory().get_audio()
face = RobotFactory().face
lights = RobotFactory().lights
    #lights = Lights(RobotFactory().get_strip())
#neck = RobotFactory().neck
#head = RobotFactory().head
wheel = RobotFactory().wheel
animations = RobotFactory().animation_manager

global_receiver = GlobalReceiver(RobotFactory().config, RobotFactory().device_manager, animations)
main_loop_sleep = RobotFactory().config.MAIN_LOOP_SLEEP
due_device = RobotFactory().device_manager.get_device(MAIN_DUE)
main_due_com = MainDueCom(RobotFactory().device_manager)

logging.info('send starting didier')

def stop(msg):
    if msg and hasattr(msg, 'key') and msg.key == RobotFactory().config.STOP_KEY:
        logging.fatal("stopping Didier")
        Misc.exec_shell("sudo halt")

while True:
    #logging.debug('run')

    try:
        msg = global_receiver.get_msg()

        if msg:
            stop(msg)
            audio.update(msg)

            #main_due_com.send_dict(msg)

            face.update(msg)
                #head.process(msg)
            wheel.update(msg)
            lights.update(msg)

        #if main_loop_sleep and main_loop_sleep != 0:
        #    time.sleep(main_loop_sleep)

        face.animate()
        lights.animate()

        wheel.check_stop(msg)
        #neck.animate()
            #wheel.process()

        #if TimeUtils.is_time(SerialDeviceManager.last_update, SerialDeviceManager.update_period):
        #    RobotFactory().device_manager.update_devices()

        #wheel.test()
        #main_due_com.get_msg()

    except Exception as err:
        logging.error('exception {}'.format(err), exc_info=True)
