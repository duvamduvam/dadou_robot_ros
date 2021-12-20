# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import sys
import logging.config

from com import Com
from audio import Audio
from neck import Neck
from mapping import Mapping
from visual import Image
from wheel import Wheel

#from lights import Lights

logging.info('Starting didier')
logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

com = Com()
mapping = Mapping()
audio = Audio(mapping)
neck = Neck()
image = Image()
wheel = Wheel()

image.load_images()

while True:
    key = com.get_msg()
    if key:
        audio.process(key)
        neck.update(key)
        wheel.update_dir(key)

    neck.process()
    wheel.process()

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

