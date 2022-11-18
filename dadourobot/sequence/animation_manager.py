import logging
import os

from dadou_utils.files.files_utils import FilesUtils
from dadou_utils.misc import Misc
from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import ANIMATION, AUDIO, AUDIOS, KEY, NECK, NECKS, FACE, FACES, LIGHTS, WHEELS, NAME, DURATION, KEYS, START, STOP

from dadourobot.robot_static import SEQUENCES_DIRECTORY
from dadourobot.sequence.animation import Animation


class AnimationManager:

    current_key = None
    playing = False
    start = False
    last_time = 0
    timeout = 0
    datas = None
    duration = 0

    audios_animation = None
    necks_animation = None
    faces_animation = None
    lights_animation = None
    wheels_animation = None

    current_animation = None

    sequences = {}

    def __init__(self):
        self.load_sequences()

    def load_sequences(self):
        sequences_files = FilesUtils.get_folder_files(SEQUENCES_DIRECTORY)
        for sequence_file in sequences_files:
            json_sequence = FilesUtils.open_json(sequence_file, 'r')
            json_sequence[NAME] = os.path.basename(sequence_file)
            self.sequences[json_sequence[KEYS]] = json_sequence

    def update(self, msg):

        if not msg or KEY not in msg or msg[KEY] not in self.sequences.keys():
            return

        animation = self.sequences[msg[KEY]]

        self.current_animation = animation
        logging.info('start animation {} with key {}'.format(self.current_animation[NAME], msg[KEY]))

        self.playing = True
        self.start = True

        self.duration = self.current_animation[DURATION]
        self.last_time = TimeUtils.current_milli_time()

        self.audios_animation = Animation(self.current_animation[AUDIOS], self.duration, AUDIOS, 1)
        self.necks_animation = Animation(self.current_animation[NECKS], self.duration, NECKS, 1)
        self.faces_animation = Animation(self.current_animation[FACES], self.duration, FACES, 1)
        self.lights_animation = Animation(self.current_animation[LIGHTS], self.duration, LIGHTS, 1)
        self.wheels_animation = Animation(self.current_animation[WHEELS], self.duration, WHEELS, 2)

    def event(self):

        if not self.playing or not self.current_animation or TimeUtils.is_time(self.last_time, self.duration):
            if self.playing:
                logging.info('stop animation')
                self.playing = False
                return {ANIMATION:False}
            return

        events = {}

        if self.start:
            events[ANIMATION] = True
            self.start = False

        #TODO improve neck
        self.fill_event(events, AUDIO, self.audios_animation)
        self.fill_event(events, NECK, self.necks_animation)
        self.fill_event(events, WHEELS, self.wheels_animation)
        self.fill_event(events, FACE, self.faces_animation)
        self.fill_event(events, LIGHTS, self.lights_animation)

        return events

    def fill_event(self, events, key, animation_type):
        if not animation_type:
            return
        event_action = animation_type.next()
        if event_action:
            events[key] = event_action

        