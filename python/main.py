import logging.config
import sys
sys.path.append('.')

from python.config import Config
from python.json_manager import JsonManager


from python.input.com import Com
from python.actions.audio import Audio
from python.actions.face import Face
from python.actions.neck import Neck
from python.actions.lights import Lights
from python.actions.wheel import Wheel

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logging.info('Starting didier')

json_manager = JsonManager()
config = Config(json_manager)
audio = Audio(json_manager)
com = Com()
face = Face(json_manager, config)
lights = Lights(json_manager, config)
neck = Neck(config)
wheel = Wheel(config)


while True:
    msg = com.get_msg()
    if msg:
        audio.process(msg)
        face.update(msg)
        neck.update(msg)
        wheel.update(msg)
        lights.update(msg)

    face.animate()
    lights.animate()
    neck.animate()
    wheel.process()
