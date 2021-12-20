# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import sys
import logging.config
import time
#logging.basicConfig(filename='didier.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

sys.path.append('classes')
from com import Com
from audio import Audio
from head import Head
from mapping import Mapping
from visual import Image
from wheel import Wheel
#from lights import Lights

logging.info('Starting didier')

com = Com()
mapping = Mapping()
audio = Audio(mapping)
head = Head()
image = Image()
wheel = Wheel()

image.load_images()

while True:
    key = com.get_msg()
    if key:
        audio.execute(key)
        head.update(key)
        wheel.update_dir(key)

    head.process()
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

