import logging.config

from dadou_utils.files.files_utils import FilesUtils
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import NAME, DURATION, LOOP, KEY, FACE, DEFAULT, \
    MOUTH_VISUALS_PATH, EYE_VISUALS_PATH, LIGHTS_PIN, BASE_PATH, MOUTHS, JSON_EXPRESSIONS, RIGHT_EYES, LEFT_EYES, \
    ANIMATION
from robot.actions.abstract_json_actions import AbstractJsonActions
from robot.sequences.sequence import Sequence
from robot.visual.image_mapping import ImageMapping
from robot.visual.visual import Visual


#TODO wrong file name

class Face(AbstractJsonActions):
    visuals = {}
    mouth_image_mapping = ImageMapping(start_pixel=0, global_width=24, global_height=16, matrix_width=8,
                                       matrix_height=8, matrix_width_nb=3, matrix_height_nb=2)

    mouth_start = 0
    mouth_end = 384
    reye_start = 385
    reye_end = 448
    leye_start = 449
    leye_end = 512

    mouth = None
    leye = None
    reye = None

    default = "default"

    element_duration = 0
    start_time = 0

    current_face = ""

    #speak_duration = 0
    #start_speak_time = 0

    def __init__(self, config, json_manager,  strip):
        super().__init__(config=config, json_manager=json_manager, json_file=config[JSON_EXPRESSIONS], action_type=FACE)
        logging.debug("start face with pin " + str(config[LIGHTS_PIN]))
        self.config = config
        self.strip = strip
        self.load_visuals()
        self.update({FACE: self.default})

    def get_expressions_sequence(self, msg):
        if msg and KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if msg and FACE in msg and msg[FACE] in self.sequences_name.keys():
            return self.sequences_name[msg[FACE]]

    def load_visuals(self):

        mouth_names = FilesUtils.get_folder_files(self.config[MOUTH_VISUALS_PATH])
        eye_names = FilesUtils.get_folder_files(self.config[EYE_VISUALS_PATH])

        for visual_path in mouth_names:
            visual = Visual(visual_path, True)
            self.visuals[visual.name] = visual

        for visual_path in eye_names:
            visual = Visual(visual_path, False)
            self.visuals[visual.name] = visual

    def get_visual(self, name):
        if name in self.visuals.keys():
            return self.visuals[name]
        else:
            logging.error("no visual name : " + name)

    #TODO record matrix array
    def fill_matrix(self, start, end, visual):
        i = start
        for x in range(0, len(visual.rgb)):
            for y in range(0, len(visual.rgb[x])):
                logging.debug(
                    "fill_matrix self.pixels[" + str(i) + "] = visual.rgb[" + str(x) + "][" + str(y) + "]")
                self.strip[i] = visual.rgb[x][y]
                i += 1

    def update(self, msg):
        logging.info("incoming msg {}".format(msg))
        #TODO improve this
        """if KEY not in msg and msg and ANIMATION in msg and not msg[ANIMATION] and not self.loop:
            self.update({FACE: self.DEFAULT})
        elif FACE not in msg:
            return msg"""

        if ANIMATION in msg and not msg[ANIMATION]:
            self.update({FACE: self.default})

        json_seq = self.get_sequence(msg, True)
        if not json_seq:
            return msg

        if self.current_face == json_seq[NAME]:
            self.start_time = TimeUtils.current_milli_time()
            return msg

        self.current_face = json_seq[NAME]

        logging.info("update face sequences : " + json_seq[NAME])

        if ANIMATION in msg and msg[ANIMATION]:
            self.loop = True
        else:
            self.loop = json_seq[LOOP]
        if DEFAULT in json_seq:
            self.default = json_seq[NAME]
        self.element_duration = json_seq[DURATION]
        self.start_time = TimeUtils.current_milli_time()
        self.mouth = Sequence(self.element_duration, self.loop, json_seq[MOUTHS], 0)
        self.leye = Sequence(self.element_duration, self.loop, json_seq[LEFT_EYES], 385) #385
        self.reye = Sequence(self.element_duration, self.loop, json_seq[RIGHT_EYES], 448) #448

        return msg

    def animate_part(self, seq: Sequence):
        change = False
        if seq.time_to_switch():
            frame = seq.get_current_element()
            logging.debug("seq.current_time : {} current element {} duration {}".format(seq.start_time, seq.current_element, seq.element_duration))
            visual = self.get_visual(frame[1])
            logging.debug("update part : " + visual.name)
            self.mouth_image_mapping.mapping(self.strip, visual.rgb, seq.start_pixel)
            #logging.debug("next sequences[" + str(seq.current_frame) + "] total : " + str(len(seq.frames)))
            seq.next()
            change = True
        return change

    #def

    def process(self):
        if not self.loop:
            if self.global_duration != 0:
                if TimeUtils.is_time(self.start_global_lime, self.global_duration):
                    self.global_duration = 0
                    self.update({FACE: DEFAULT})
            else:
                if self.start_time != 0 and TimeUtils.is_time(self.start_time, self.element_duration):
                    self.update({FACE: DEFAULT})
        #if self.speak_duration != 0:
        #    if TimeUtils.is_time(self.start_speak_time, self.speak_duration):
        #        self.speak_duration = 0
        #        self.loop = False

        if self.animate_part(self.mouth) or self.animate_part(self.leye) or self.animate_part(self.reye):
            self.strip.show()


#class Frame:

#    def __init__(self, t, name):
#        self.duration = t
#        self.name = name

