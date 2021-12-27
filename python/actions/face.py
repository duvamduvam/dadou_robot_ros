import logging.config
from python.tests.conf_test import TestSetup
import time
from operator import mod

import board
import neopixel

from python.json_manager import JsonManager
from python.utils import Utils
from python.visual import Visual


class Face:
    visuals = []
    json_manager = JsonManager()

    mouth_start = 0
    mouth_end = 384
    reye_start = 385
    reye_end = 448
    leye_start = 449
    leye_end = 512

    pixels = neopixel.NeoPixel(board.D18, (8 * 8 * 8)+1, auto_write=False)
    pixels.brightness = 0.1

    mouth_seq = []
    leye_seq = []
    reye_seq = []
    loop = False
    time = 0

    def __init__(self):
        self.load_visual()

    def load_visual(self):
        visuals_path = self.json_manager.get_all_visual()
        for visual_path in visuals_path:
            self.visuals.append(Visual(visual_path['name'], visual_path['path']))

    def fill_matrix(self, start, end, visual):
        i = start
        for x in range(0, len(visual.rgb)):
            for y in range(0, len(visual.rgb[x])):
                logging.debug(
                    "fill_matrix self.pixels[" + str(i) + "] = visual.rgb[" + str(x) + "][" + str(y) + "]")
                self.pixels[i] = visual.rgb[x][y]
                i += 1

    def fill_mouth(self, visual):
        self.fill_matrix(self.mouth_start, self.mouth_end, visual)

    def load_seq_part(self, name):
        json_seq = self.json_manager.get_part_seq(name)

        target = []
        frames = []
        for s in json_seq['sequence']:
            frames.append(Frame(s['time'], s['name']))

        return Sequence(json_seq['time'], json_seq['loop'], frames)

    def update(self, key):
        json_seq = self.json_manager.get_face_seq(key)
        self.loop = json_seq['loop']
        self.time = json_seq['time']
        self.mouth_seq = self.load_seq_part(json_seq['mouth'])
        self.leye_seq = self.load_seq_part(json_seq['reye'])
        self.reye_seq = self.load_seq_part(json_seq['leye'])

    def animate_part(self, seq, start, end):
        frame = seq.frames[seq.current_frame]
        if Utils.is_time(seq.current_time, frame.time):
            visual = Visual.get_visual(frame.name, self.visuals)
            self.fill_matrix(start, end, visual)
            seq.current_frame = seq.current_frame % len(seq.frames)
            seq.current_time = time.time()
            self.pixels.show()

    def animate(self):
        self.animate_part(self.mouth_seq, self.mouth_start, self.mouth_end)
        self.animate_part(self.reye_seq, self.reye_start, self.reye_end)
        self.animate_part(self.leye_seq, self.leye_start, self.leye_end)


class Sequence:
    duration = 0
    current_time = time.time()
    loop = False
    frames = []
    current_frame = 0

    def __init__(self, duration, loop, frames):
        self.duration = duration
        self.loop = loop
        self.frames = frames


class Frame:

    def __init__(self, t, name):
        self.time = t
        self.name = name
