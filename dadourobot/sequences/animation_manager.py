import logging
import os
import random

from dadou_utils.files.files_utils import FilesUtils
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import ANIMATION, STOP_ANIMATION_KEYS, AUDIO, AUDIOS, KEY, NECK, NECKS, FACE, FACES, LIGHTS, WHEELS, NAME, \
    DURATION, KEYS, RANDOM, START, STOP, TYPES, SEQUENCES_DIRECTORY, LOOP_DURATION, RANDOM_ANIMATION_LOW, RANDOM_ANIMATION_HIGH, BASE_PATH, \
    LEFT_ARM, RIGHT_ARM

from dadourobot.actions.abstract_actions import ActionsAbstract
from dadourobot.sequences.animation import Animation
from dadourobot.sequences.random_animation_start import RandomAnimationStart


class AnimationManager(ActionsAbstract):

    current_key = None
    playing = False
    start = False

    last_time = 0
    timeout = 0
    random_duration = 0
    last_random = 0

    datas = None
    duration = 0

    audios_animation = None
    left_arm_animation = None
    right_arm_animation = None
    necks_animation = None
    faces_animation = None
    lights_animation = None
    wheels_animation = None

    current_animation = None

    def __init__(self, config, json_manager):
        self.config = config
        super().__init__(json_manager, None)
        self.load_animation_sequences()
        self.stop_keys = self.config[STOP_ANIMATION_KEYS]
        self.random_duration = random.randint(self.config[RANDOM_ANIMATION_LOW], self.config[RANDOM_ANIMATION_HIGH])
        RandomAnimationStart.value = TimeUtils.current_milli_time()
        logging.info("random duration time {}".format(self.random_duration))


    def load_animation_sequences(self):
        sequences_files = FilesUtils.get_folder_files(self.config[BASE_PATH]+self.config[SEQUENCES_DIRECTORY])
        for sequence_file in sequences_files:
            json_sequence = FilesUtils.open_json(sequence_file, 'r')
            json_sequence[NAME] = os.path.basename(sequence_file)
            self.sequences_key[json_sequence[KEYS]] = json_sequence
            self.sequences_name[json_sequence[NAME]] = json_sequence


    def random(self):
        if TimeUtils.is_time(RandomAnimationStart.value, self.random_duration):
            random_seq_names = []
            for seq_key in self.sequences_name.keys():
                sequence = self.sequences_name[seq_key]
                if TYPES in sequence.keys():
                    for t in sequence[TYPES]:
                        if t == RANDOM:
                            random_seq_names.append(sequence[NAME])

            if len(random_seq_names) > 0:
                random_index = random.randint(0, len(random_seq_names)-1)
                RandomAnimationStart.value = TimeUtils.current_milli_time()
                self.update({ANIMATION: random_seq_names[random_index]})
                self.random_duration = random.randint(self.config[RANDOM_ANIMATION_LOW],
                                                      self.config[RANDOM_ANIMATION_HIGH])
                logging.info('random animation {}'.format(random_seq_names[random_index]))

    def update(self, msg):
        #if msg and KEY in msg.keys() and msg[KEY] in self.stop_keys:
        #    self.duration = 0
        #    return

        animation = self.get_sequence(msg, ANIMATION, False)
        if not animation:
            self.duration = 0
            return

        self.current_animation = animation
        logging.info('start animation {}'.format(self.current_animation[NAME]))

        self.playing = True
        self.start = True

        self.duration = self.current_animation[DURATION]
        self.last_time = TimeUtils.current_milli_time()
        self.last_random = TimeUtils.current_milli_time()

        self.audios_animation = Animation(self.current_animation, self.duration, AUDIOS, 1)
        self.left_arm_animation = Animation(self.current_animation, self.duration, LEFT_ARM, 1)
        self.right_arm_animation = Animation(self.current_animation, self.duration, RIGHT_ARM, 1)
        self.necks_animation = Animation(self.current_animation, self.duration, NECK, 1)
        self.faces_animation = Animation(self.current_animation, self.duration, FACES, 1)
        self.lights_animation = Animation(self.current_animation, self.duration, LIGHTS, 1)
        self.wheels_animation = Animation(self.current_animation, self.duration, WHEELS, 2)

    def event(self):
        if not self.playing or not self.current_animation or TimeUtils.is_time(self.last_time, self.duration):
            if self.playing:
                logging.info('stop animation')
                self.playing = False
                return {ANIMATION: False}
            return

        events = {}

        if self.start:
            events[ANIMATION] = True
            events[LOOP_DURATION] = self.duration
            self.start = False

        #TODO improve neck
        self.fill_event(events, AUDIO, self.audios_animation)
        self.fill_event(events, LEFT_ARM, self.left_arm_animation)
        self.fill_event(events, RIGHT_ARM, self.right_arm_animation)
        self.fill_event(events, NECK, self.necks_animation)
        self.fill_event(events, WHEELS, self.wheels_animation)
        self.fill_event(events, FACE, self.faces_animation)
        self.fill_event(events, LIGHTS, self.lights_animation)
        if len(events) > 0:
            logging.info('udpate animation {}'.format(self.current_animation[NAME]))
        return events

    def fill_event(self, events, key, animation):
        if not animation or not animation.has_data:
            return
        event_action = animation.next()
        if event_action:
            events[key] = event_action

        