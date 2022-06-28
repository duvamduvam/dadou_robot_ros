import logging.config
import sys

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
#head = Head()
#face = Face()
#lights = Lights()
neck = Neck()
wheel = Wheel()

global_receiver = GlobalReceiver()

while True:
    #wheel.test()
    msg = global_receiver.get_msg()
    if msg:
        audio.process(msg)
        #head.process(msg)
        #face.update(msg)
        #neck.update(msg)
        #wheel.update(msg.left_wheel, msg.right_wheel)
        #lights.update(msg)


    #face.animate()
    #lights.animate()
    #neck.animate()
    #wheel.process()
