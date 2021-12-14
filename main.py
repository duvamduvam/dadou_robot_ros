# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging, sys, logging.config
#logging.basicConfig(filename='didier.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)

sys.path.append('classes')
from com import Com
from audio import Audio
from audio2 import Audio2
from mapping import Mapping
#from lights import Lights


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


logging.info('Starting didier')

if __name__ == '__main__':
    print_hi('Start didier')

com = Com()
audio = Audio2()
mapping = Mapping()
#lights = Lights()

audioPath = mapping.get_audio_file("A5")
#lights.fade_red()


if audioPath:
    audio.play(audioPath)

logging.info("test")

#while True:
#    //msg = com.getMsg()

