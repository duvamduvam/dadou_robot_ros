import logging.config

from dadou_utils.files.files_manager import FilesUtils
from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import NAME, DURATION, LOOP, KEY, KEYS, FACE

from dadourobot.actions.sequence import Sequence
from dadourobot.robot_static import MOUTHS, LEYE, REYE, JSON_EXPRESSIONS
from dadourobot.visual.image_mapping import ImageMapping
from dadourobot.visual.visual import Visual


class Face:
    visuals = []
    image_mapping = ImageMapping(8, 8, 3, 2)

    mouth_start = 0
    mouth_end = 384
    reye_start = 385
    reye_end = 448
    leye_start = 449
    leye_end = 512

    mouth = None
    leye = None
    reye = None

    sequences_key = {}
    sequences_name = {}

    DEFAULT = "default"

    duration = 0
    loop = False
    start_time = 0

    def __init__(self, json_manager, config, strip):
        self.config = config
        self.json_manager = json_manager
        logging.info("start face with pin " + str(self.config.FACE_PIN))
        self.strip = strip
        self.load_sequences()
        self.load_visuals()
        self.update({KEY:self.DEFAULT})

    def load_sequences(self):
        expression_sequences = self.json_manager.open_json(JSON_EXPRESSIONS)
        for seq in expression_sequences:
            for key in seq[KEYS]:
                self.sequences_key[key] = seq
            self.sequences_name[seq[NAME]] = seq

    def get_expressions_sequence(self, msg):
        if msg and KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if msg and FACE in msg and msg[FACE] in self.sequences_name.keys():
            return self.sequences_name[msg[FACE]]

    def load_visuals(self):
        mouth_visuals_path = self.config.MOUTH_VISUALS_PATH
        eye_visuals_path = self.config.EYE_VISUALS_PATH

        mouth_names = FilesUtils.get_folder_files(mouth_visuals_path)
        eye_names = FilesUtils.get_folder_files(eye_visuals_path)

        for visual_path in mouth_names:
            self.visuals.append(Visual(visual_path, True))

        for visual_path in eye_names:
            self.visuals.append(Visual(visual_path, False))

    def get_visual(self, name):
        for visual in self.visuals:
            if visual.name in name:
                return visual
        logging.error("no visual name : " + name)

    def fill_matrix(self, start, end, visual):
        i = start
        for x in range(0, len(visual.rgb)):
            for y in range(0, len(visual.rgb[x])):
                logging.debug(
                    "fill_matrix self.pixels[" + str(i) + "] = visual.rgb[" + str(x) + "][" + str(y) + "]")
                self.strip[i] = visual.rgb[x][y]
                i += 1

    def update(self, msg):
        json_seq = self.get_expressions_sequence(msg)
        if not json_seq:
            return

        logging.info("update face sequence : " + json_seq[NAME])
        self.duration = json_seq[DURATION]
        self.loop = json_seq[LOOP]
        self.start_time = TimeUtils.current_milli_time()
        self.mouth = Sequence(self.duration, self.loop, json_seq[MOUTHS], 0)
        self.leye = Sequence(self.duration, self.loop, json_seq[LEYE], 385) #385
        self.reye = Sequence(self.duration, self.loop, json_seq[REYE], 448) #448

    def animate_part(self, seq: Sequence):
        change = False
        if seq.time_to_switch():
            seq.next()
            frame = seq.get_current_element()
            #logging.info("seq.current_time : {} current element {} duration {}".format(seq.start_time, seq.current_element, seq.element_duration*seq.duration))
            visual = self.get_visual(frame[1])
            #logging.debug("update part : " + visual.name)
            self.image_mapping.mapping(self.strip, visual.rgb, seq.start_pixel)
            #logging.debug("next sequence[" + str(seq.current_frame) + "] total : " + str(len(seq.frames)))
            change = True
        return change

    def animate(self):

        if self.start_time != 0 and not self.loop and \
                TimeUtils.is_time(self.start_time, self.duration):
            self.update({KEY: self.DEFAULT})
        if self.animate_part(self.mouth) or self.animate_part(self.leye) or self.animate_part(self.reye):
            self.strip.show()


#class Frame:

#    def __init__(self, t, name):
#        self.duration = t
#        self.name = name

