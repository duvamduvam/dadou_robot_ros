# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging.config

import sys
sys.path.append('.')

from python.com import Com
from python.actions.audio import Audio
from python.actions.neck import Neck
from python.mapping import Mapping
from python.actions.lights import Lights
from python.actions.wheel import Wheel

#from lights import Lights
logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logging.info('Starting didier')


com = Com()
mapping = Mapping()
audio = Audio(mapping)
neck = Neck()
#image = Image()
wheel = Wheel()
lights = Lights()

while True:
    key = com.get_msg()
    if key:
        audio.update(key)
        neck.update(key)
        wheel.update(key)
        lights.update(key)

    neck.animate()
    wheel.process()
    lights.animate()

#lights = Lights()

#audioPath = mapping.get_audio_file("A5")
#lights.fade_red()
#if audioPath:
#    audio.play_sound(audioPath)

#time.sleep(10)
#audio.stop_sound()
#audioPath = mapping.get_audio_file("A3")
#lights.fade_red()

#audio.stop_sound2()
#if audioPath:
#    audio.play_sound(audioPath)



#while True:
#    //msg = com.getMsg()

