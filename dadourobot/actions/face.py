import logging.config

from dadou_utils.files.files_manager import FilesUtils
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import NAME, DURATION, LOOP, KEY, FACE, SPEAK, SPEAK_DURATION, DEFAULT

from actions.abstract_actions import ActionsAbstract
from sequences.random_animation_start import RandomAnimationStart
from sequences.sequence import Sequence
from robot_config import MOUTHS, LEYE, REYE, JSON_EXPRESSIONS, LOOP_DURATION
from visual.image_mapping import ImageMapping
from visual.visual import Visual

from dadourobot.robot_config import MOUTH_VISUALS_PATH, EYE_VISUALS_PATH, LIGHTS_PIN, BASE_PATH


#TODO wrong file name

class Face(ActionsAbstract):
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

    DEFAULT = "default"

    duration = 0
    start_time = 0

    #speak_duration = 0
    #start_speak_time = 0


    def __init__(self, json_manager,  strip):
        super().__init__(json_manager, JSON_EXPRESSIONS)
        logging.info("start face with pin " + str(LIGHTS_PIN))
        self.strip = strip
        self.load_visuals()
        self.update({FACE: self.DEFAULT})

    def get_expressions_sequence(self, msg):
        if msg and KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if msg and FACE in msg and msg[FACE] in self.sequences_name.keys():
            return self.sequences_name[msg[FACE]]

    def load_visuals(self):

        mouth_names = FilesUtils.get_folder_files(BASE_PATH+MOUTH_VISUALS_PATH)
        eye_names = FilesUtils.get_folder_files(BASE_PATH+EYE_VISUALS_PATH)

        for visual_path in mouth_names:
            self.visuals.append(Visual(visual_path, True))

        for visual_path in eye_names:
            self.visuals.append(Visual(visual_path, False))

    def get_visual(self, name):
        for visual in self.visuals:
            if visual.name in name:
                return visual
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

    """def speak_during_audio(self, msg):
        if not msg: return
        if SPEAK in msg.keys():
            if SPEAK_DURATION not in msg.keys():
                logging.error("no duration for speak sequences")
            else:
                speak_seq = self.sequences_name[SPEAK]
                self.speak_duration = msg[SPEAK_DURATION]
                self.start_speak_time = TimeUtils.current_milli_time()
                speak_seq[LOOP] = True
                return speak_seq"""

    """def check_input(self, msg):
        sequence = self.get_sequence(msg, FACE, True)
        if sequence:
            if LOOP_DURATION in msg.keys():
                sequence[LOOP] = True
                self.loop_duration = msg[LOOP_DURATION]
                self.start_loop_duration = TimeUtils.current_milli_time()
            return sequence

        #speak_seq = self.speak_during_audio(msg)
        #if speak_seq : return speak_seq"""

    def update(self, msg):
        json_seq = self.get_sequence(msg, FACE, True)
        if not json_seq: return

        logging.info("update face sequences : " + json_seq[NAME])
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
            logging.debug("seq.current_time : {} current element {} duration {}".format(seq.start_time, seq.current_element, seq.element_duration*seq.duration))
            visual = self.get_visual(frame[1])
            #logging.debug("update part : " + visual.name)
            self.image_mapping.mapping(self.strip, visual.rgb, seq.start_pixel)
            #logging.debug("next sequences[" + str(seq.current_frame) + "] total : " + str(len(seq.frames)))
            change = True
        return change

    #def

    def animate(self):
        if self.loop_duration != 0:
            if TimeUtils.is_time(self.start_loop_duration, self.loop_duration):
                self.loop_duration = 0
                self.loop = False
        #if self.speak_duration != 0:
        #    if TimeUtils.is_time(self.start_speak_time, self.speak_duration):
        #        self.speak_duration = 0
        #        self.loop = False
        if self.start_time != 0 and not self.loop and \
                TimeUtils.is_time(self.start_time, self.duration):
            self.update({FACE: DEFAULT})
        if self.animate_part(self.mouth) or self.animate_part(self.leye) or self.animate_part(self.reye):
            self.strip.show()


#class Frame:

#    def __init__(self, t, name):
#        self.duration = t
#        self.name = name

