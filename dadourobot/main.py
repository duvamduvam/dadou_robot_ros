import logging.config
import sys

from dadou_utils.com.serial_devices_manager import SerialDeviceManager
from dadou_utils.time.time_utils import TimeUtils

import time

#sys.path.append('..')

from dadou_utils.misc import Misc

#from dadourobot.sequence.animation_manager import AnimationManager
from dadourobot.robot_static import RobotStatic
from dadourobot.sequence.animation_manager import AnimationManager



from dadourobot.actions.audio_manager import AudioManager
from dadourobot.actions.head import Head
from dadourobot.robot_factory import RobotFactory
from dadourobot.input.global_receiver import GlobalReceiver


print(sys.path)

from dadourobot.actions.face import Face
from dadourobot.actions.neck import Neck
from dadourobot.actions.lights import Lights
from dadourobot.actions.wheel import Wheel

logging.info('Starting didier')


RobotFactory()
audio = AudioManager()
    #face = Face(RobotFactory().get_strip())
    #lights = Lights(RobotFactory().get_strip())
    #neck = Neck()
head = RobotFactory().head
    #wheel = Wheel()
#animations = AnimationManager()

global_receiver = GlobalReceiver(RobotFactory().device_manager)
main_loop_sleep = RobotFactory().config.MAIN_LOOP_SLEEP
due_device = RobotFactory().device_manager.get_device(RobotStatic.MAIN_DUE)

def stop(msg):
    if msg and hasattr(msg, 'key') and msg.key == RobotFactory().config.STOP_KEY:
        logging.fatal("stopping Didier")
        Misc.exec_shell("sudo halt")

while True:
    try:
        msg = global_receiver.get_msg()
        if msg:
            stop(msg)
            due_device.send_msg("   "+msg, True)
            #animations.update(msg.key)
            audio.process(msg)
                #face.update(msg.key)
                #head.process(msg)
                #wheel.update(msg.left_wheel, msg.right_wheel)
                #lights.update(msg.key)

        if main_loop_sleep and main_loop_sleep != 0:
            time.sleep(main_loop_sleep)

            #animations.process()
            #face.animate()
            #lights.animate()
            #neck.animate()
            #wheel.process()

        if TimeUtils.is_time(SerialDeviceManager.last_update, SerialDeviceManager.update_period):
            RobotFactory().device_manager.update_devices()

    except Exception as err:
        logging.error('exception {}'.format(err))
