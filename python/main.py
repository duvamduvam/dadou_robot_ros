import logging.config

import sys

from python.config import MConfig
from python.json_manager import JsonManager

sys.path.append('.')

from python.com import Com
from python.actions.audio import Audio
from python.actions.face import Face
from python.actions.neck import Neck
from python.actions.lights import Lights
from python.actions.wheel import Wheel

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logging.info('Starting didier')

json_manager = JsonManager()
config = MConfig(json_manager)
audio = Audio(json_manager)
com = Com()
face = Face(json_manager)
lights = Lights(json_manager)
neck = Neck()
wheel = Wheel()


while True:
    key = com.get_msg()
    if key:
        audio.process(key)
        face.update(key)
        neck.update(key)
        wheel.update(key)
        lights.update(key)

    face.animate()
    lights.animate()
    neck.animate()
    wheel.process()