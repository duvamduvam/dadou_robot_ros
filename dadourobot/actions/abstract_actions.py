import logging
import random

from dadou_utils.time.time_utils import TimeUtils
from dadou_utils.utils_static import KEY, KEYS, NAME, LOOP

from robot_static import RANDOM_ANIMATION_LOW, RANDOM_ANIMATION_HIGH, LOOP_DURATION


class ActionsAbstract:

    loop_duration = 0
    start_loop_duration = 0
    loop = False

    def __init__(self, json_manager, config, json_key=None):
        self.json_manager = json_manager
        self.sequences_key = {}
        self.sequences_name = {}
        self.random_duration = random.randint(config.get(RANDOM_ANIMATION_LOW), config.get(RANDOM_ANIMATION_HIGH))
        self.last_random = TimeUtils.current_milli_time()
        if json_key : self.load_sequences(json_key)

    def load_sequences(self, json_key):
        sequences = self.json_manager.open_json(json_key)
        for seq in sequences:
            if KEYS in seq.keys():
                for key in seq[KEYS]:
                    self.sequences_key[key] = seq
            self.sequences_name[seq[NAME]] = seq

    def get_sequence(self, msg, sequence_key, animation_loop):
        if msg and KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if msg and sequence_key in msg and msg[sequence_key] in self.sequences_name.keys():
            sequence = self.sequences_name[msg[sequence_key]]
            if animation_loop and LOOP_DURATION in msg.keys():
                sequence[LOOP] = True
                self.loop_duration = msg[LOOP_DURATION]
                self.start_loop_duration = TimeUtils.current_milli_time()
            return sequence
        logging.debug("no sequence with key {}".format(sequence_key))

    """def get_sequence_from_input(self, msg, sequence_key):
        if not msg:
            return
        if KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if sequence_key in msg and msg[sequence_key] in self.sequences_name.keys():
            logging.error("no {} in ".format(msg[sequence_key], sequence_key))
            return self.sequences_name[msg[sequence_key]]"""