import logging.config

from dadou_utils.files.files_manager import FilesUtils
from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import NAME, DURATION, LOOP

from dadourobot.actions.sequence import Sequence
from dadourobot.robot_static import MOUTHS, LEYE, REYE
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

    DEFAULT = "default"

    duration = 0
    loop = False
    start_time = 0

    def __init__(self, json_manager, config, strip):
        self.config = config
        self.json_manager = json_manager
        logging.info("start face with pin " + str(self.config.FACE_PIN))
        self.strip = strip
        self.load_visuals()
        self.update(self.DEFAULT)

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

    def update(self, key):
        if key:
            json_seq = self.json_manager.get_face_seq(key)
            if json_seq:
                logging.info("update face sequence : " + json_seq[NAME])
                self.duration = json_seq[DURATION]
                self.loop = json_seq[LOOP]
                self.start_time = TimeUtils.current_milli_time()
                self.mouth = Sequence(self.duration, self.loop, json_seq[MOUTHS], 0)
                self.leye = Sequence(self.duration, self.loop, json_seq[LEYE], 257) #385
                self.reye = Sequence(self.duration, self.loop, json_seq[REYE], 320) #448

    def animate_part(self, seq: Sequence):
        change = False
        if seq.time_to_switch():
            seq.next()
            frame = seq.get_current_element()
            # logging.debug("seq.current_time : " + str(seq.current_time) + " frame.time " + str(frame.time))
            visual = self.get_visual(frame[0])
            # logging.debug("update part : " + visual.name)
            self.image_mapping.mapping(self.strip, visual.rgb, seq.start_pixel)
            # logging.debug("next sequence[" + str(seq.current_frame) + "] total : " + str(len(seq.frames)))
            change = True
        return change

    def animate(self):

        if self.start_time != 0 and not self.loop and \
                TimeUtils.is_time(self.start_time, self.duration):
            self.update(self.DEFAULT)
        if self.animate_part(self.mouth) or self.animate_part(self.leye) or self.animate_part(self.reye):
            self.strip.show()


#class Frame:

#    def __init__(self, t, name):
#        self.duration = t
#        self.name = name

