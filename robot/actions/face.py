import logging.config

from dadou_utils_ros.files.files_utils import FilesUtils
from dadou_utils_ros.utils.time_utils import TimeUtils
from robot.robot_static import MOUTH_VISUALS_PATH, EYE_VISUALS_PATH, LIGHTS_PIN, MOUTHS, \
    RIGHT_EYES, LEFT_EYES
from dadou_utils_ros.utils_static import NAME, DURATION, LOOP, KEY, FACE, DEFAULT, BASE_PATH, \
    JSON_EXPRESSIONS, ANIMATION, STOP
from robot.actions.abstract_json_actions import AbstractJsonActions
from robot.sequences.sequence import Sequence
from robot.visual.image_mapping import ImageMapping
from robot.visual.visual import Visual


#TODO wrong file name

class Face(AbstractJsonActions):
    # Les tables ImageMapping sont immuables (construites une fois, jamais mutées) :
    # elles restent au niveau classe. `visuals` (dict rempli à load_visuals) est en
    # revanche un état mutable -> initialisé par instance dans __init__ (piège Python).
    mouth_image_mapping = ImageMapping.mouth()
    eye_image_mapping = ImageMapping.eye()

    # Zones du strip (source unique). Yeux nommés VU DE FACE (spectateur) :
    # la mire couleurs du 2026-07-11 a montré que les pistes left/right
    # étaient croisées. Câblage CONTIGU, sans trous (mire bordure) :
    # bouche 0-383, œil droit 384-447, œil gauche 448-511. Les anciens
    # starts 385/449 décalaient tout le contenu d'une LED (« animations
    # 6x6 collées à gauche »).
    MOUTH_START = 0
    LEYE_START = 448
    REYE_START = 384

    mouth = None
    leye = None
    reye = None

    default = "default"

    element_duration = 0
    start_time = 0

    current_face = ""

    def __init__(self, config, json_manager,  strip):
        super().__init__(config=config, json_manager=json_manager, json_file=config[JSON_EXPRESSIONS], action_type=FACE)
        logging.debug("start face with pin " + str(config[LIGHTS_PIN]))
        self.visuals = {}
        self.config = config
        self.strip = strip
        self.load_visuals()
        self.update({FACE: self.default})

    def load_visuals(self):

        mouth_names = FilesUtils.get_folder_files(self.config[MOUTH_VISUALS_PATH])
        eye_names = FilesUtils.get_folder_files(self.config[EYE_VISUALS_PATH])

        for visual_path in mouth_names + eye_names:
            visual = Visual(visual_path)
            self.visuals[visual.name] = visual

    def get_visual(self, name):
        if name in self.visuals.keys():
            return self.visuals[name]
        else:
            logging.error("no visual name : " + name)

    def parts(self):
        # Chaque partie rend avec SA table : la bouche (serpentin 6 matrices)
        # et les yeux (matrice unique) n'ont pas le même câblage.
        return ((self.mouth, self.mouth_image_mapping),
                (self.leye, self.eye_image_mapping),
                (self.reye, self.eye_image_mapping))

    def update(self, msg):
        logging.info("incoming msg {}".format(msg))

        if msg[FACE] == STOP:
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
        self.mouth = Sequence(self.element_duration, self.loop, json_seq[MOUTHS], self.MOUTH_START)
        self.leye = Sequence(self.element_duration, self.loop, json_seq[LEFT_EYES], self.LEYE_START)
        self.reye = Sequence(self.element_duration, self.loop, json_seq[RIGHT_EYES], self.REYE_START)
        self.show_first_frames()

        return msg

    def show_first_frames(self):
        # Dessine tout de suite la première frame de chaque partie : sans ça,
        # une frame n'apparaît qu'à son premier time_to_switch() — les yeux d'une
        # piste à frame unique restaient sur l'expression PRÉCÉDENTE pendant
        # toute la durée de la séquence (2 à 8 s de visage périmé à chaque bascule).
        for seq, mapping in self.parts():
            if not seq.elements:
                continue
            visual = self.get_visual(seq.get_current_element()[1])
            if visual is not None:
                mapping.mapping(self.strip, visual.rgb, seq.start_pixel)
        self.strip.show()

    def animate_part(self, seq: Sequence, mapping: ImageMapping):
        change = False
        if seq.time_to_switch():
            frame = seq.get_current_element()
            logging.debug("seq.current_time : {} current element {} duration {}".format(seq.start_time, seq.current_element, seq.element_duration))
            visual = self.get_visual(frame[1])
            if visual is not None:
                mapping.mapping(self.strip, visual.rgb, seq.start_pixel)
            seq.next()
            change = True
        return change

    def process(self):
        if not self.loop:
            if self.global_duration != 0:
                if TimeUtils.is_time(self.start_global_lime, self.global_duration):
                    self.global_duration = 0
                    self.update({FACE: DEFAULT})
            else:
                if self.start_time != 0 and TimeUtils.is_time(self.start_time, self.element_duration):
                    self.update({FACE: DEFAULT})

        # PAS de court-circuit : chaque partie doit avancer à chaque tick,
        # d'où le or bit à bit sur les trois résultats.
        change = False
        for seq, mapping in self.parts():
            change |= self.animate_part(seq, mapping)
        if change:
            self.strip.show()

