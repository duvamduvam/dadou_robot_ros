import logging.config
import sys
import traceback

from dadou_utils.com.serial_devices_manager import SerialDeviceManager
from dadou_utils.time.time_utils import TimeUtils

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
neck = Neck()
#head = RobotFactory().head
wheel = RobotFactory().wheel
#animations = AnimationManager()

global_receiver = GlobalReceiver(RobotFactory().device_manager)
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
            #main_due_com.send_dict(msg)
            #animations.update(msg.key)
            audio.process(msg)
                #face.update(msg.key)
                #head.process(msg)
            wheel.update(msg)
            lights.update(msg.key)

        if main_loop_sleep and main_loop_sleep != 0:
            time.sleep(main_loop_sleep)

            #animations.process()
        face.animate()
        lights.animate()
        neck.animate()
            #wheel.process()

        #if TimeUtils.is_time(SerialDeviceManager.last_update, SerialDeviceManager.update_period):
        #    RobotFactory().device_manager.update_devices()

        #wheel.test()
        #main_due_com.get_msg()

    except Exception as err:
        logging.error('exception {}'.format(err))
        traceback.print_exc()
