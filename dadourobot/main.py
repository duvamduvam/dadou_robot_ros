import logging.config
import sys
import time

from dadou_utils.misc import Misc

sys.path.append('..')

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
head = Head()
wheel = Wheel()

global_receiver = GlobalReceiver()

main_loop_sleep = RobotFactory().config.MAIN_LOOP_SLEEP


def stop(msg):
    if msg and hasattr(msg, 'key') and msg.key == RobotFactory().config.STOP_KEY:
        logging.fatal("stopping Didier")
        Misc.exec_shell("sudo halt")

while True:
    #wheel.test()
    msg = global_receiver.get_msg()
    if msg:
        stop(msg)
        audio.process(msg)
        #face.update(msg.key)
        head.process(msg)
        #wheel.update(msg.left_wheel, msg.right_wheel)
        #lights.update(msg.key)

    if main_loop_sleep and main_loop_sleep != 0:
        time.sleep(main_loop_sleep)

    #face.animate()
    #lights.animate()
    #neck.animate()
    #wheel.process()


