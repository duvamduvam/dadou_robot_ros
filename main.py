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
from mapping import Mapping
from visual import Image
#from lights import Lights


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


logging.info('Starting didier')

if __name__ == '__main__':
    print_hi('Start didier')

com = Com()
audio = Audio()
mapping = Mapping()
image = Image()

image.load_images()

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

