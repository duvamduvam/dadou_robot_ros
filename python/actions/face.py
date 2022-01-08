import logging.config
import neopixel
from microcontroller import Pin

from python.config import Config
from python.visual.image_mapping import ImageMapping
from python.json_manager import JsonManager
from python.sequence import Sequence
from python.utils import Utils
from python.visual.visual import Visual


class Face:
    visuals = []
    image_mapping = ImageMapping(8, 8, 3, 2)

    mouth_start = 0
    mouth_end = 384
    reye_start = 385
    reye_end = 448
    leye_start = 449
    leye_end = 512

    mouth_seq = []
    leye_seq = []
    reye_seq = []
    loop = False
    duration = 0
    start_time = 0

    def __init__(self, json_manager: JsonManager, config: Config):
        logging.debug("start face with pin " + str(config.FACE_PIN))
        self.pixels = neopixel.NeoPixel(Pin(config.FACE_PIN), self.leye_end + 1, auto_write=False)
        self.pixels.brightness = 0.1
        self.json_manager = json_manager
        self.load_visuals()

    def load_visuals(self):
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

    def load_seq_part(self, name):
        json_seq = self.json_manager.get_part_seq(name)
        frames = []
        for s in json_seq[JsonManager.SEQUENCE]:
            frames.append(Frame(s['duration'], s['name']))

        return Sequence(json_seq['duration'], json_seq[JsonManager.LOOP], frames)

    def update(self, key):
        json_seq = self.json_manager.get_face_seq(key)
        if json_seq:
            logging.info("update face sequence : " + key)
            self.loop = json_seq[JsonManager.LOOP]
            self.duration = json_seq['duration']
            self.mouth_seq = self.load_seq_part(json_seq['mouth'])
            self.leye_seq = self.load_seq_part(json_seq['reye'])
            self.reye_seq = self.load_seq_part(json_seq['leye'])
            self.start_time = Utils.current_milli_time()

    def animate_part(self, seq):
        if Utils.is_time(seq.start_time, seq.duration):
            seq.next()
            frame = seq.current_element
            # logging.debug("seq.current_time : " + str(seq.current_time) + " frame.time " + str(frame.time))
            visual = Visual.get_visual(frame.name, self.visuals)
            # logging.debug("update part : " + visual.name)
            self.image_mapping.mapping(self.pixels, visual.rgb)
            # logging.debug("next sequence[" + str(seq.current_frame) + "] total : " + str(len(seq.frames)))

    def animate(self):
        if not self.loop and Utils.is_time(self.start_time, self.duration):
            self.update('default')
        self.animate_part(self.mouth_seq)
        # self.animate_part(self.reye_seq, self.reye_start, self.reye_end)
        # self.animate_part(self.leye_seq, self.leye_start, self.leye_end)
        self.pixels.show()


class Frame:

    def __init__(self, t, name):
        self.duration = t
        self.name = name
