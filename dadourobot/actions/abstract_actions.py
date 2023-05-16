import logging
import random

from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import KEY, KEYS, NAME, LOOP, RANDOM_ANIMATION_LOW, RANDOM_ANIMATION_HIGH, LOOP_DURATION


class ActionsAbstract:

    loop_duration = 0
    start_loop_duration = 0
    loop = False

    def __init__(self, json_manager, json_key):
        self.json_manager = json_manager
        self.sequences_key = {}
        self.sequences_name = {}
        self.msg_time = 0


        if json_key:
            self.load_sequences(json_key)

    def load_sequences(self, json_key):
        sequences = self.json_manager.open_json(json_key)
        for seq in sequences:
            if KEYS in seq.keys():
                for key in seq[KEYS]:
                    self.sequences_key[key] = seq
            self.sequences_name[seq[NAME]] = seq

    def get_sequence(self, msg, sequence_type, animation_loop):

        sequence = self.get_sequence_by_key(msg, sequence_type, self.sequences_name)
        if not sequence:
            sequence = self.get_sequence_by_key(msg, KEY, self.sequences_key)

        if sequence:
            if animation_loop and LOOP_DURATION in msg.keys():
                sequence[LOOP] = True
                self.loop_duration = msg[LOOP_DURATION]
                self.start_loop_duration = TimeUtils.current_milli_time()
            return sequence
        else:
           logging.debug("no sequence with key {}".format(sequence_type))

    def get_sequence_by_key(self, msg, input_key, sequence_values):

        if msg and input_key in msg.keys():
            if msg[input_key] in sequence_values.keys():
                return sequence_values[msg[input_key]]


    """def get_sequence_from_input(self, msg, sequence_key):
        if not msg:
            return
        if KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if sequence_key in msg and msg[sequence_key] in self.sequences_name.keys():
            logging.error("no {} in ".format(msg[sequence_key], sequence_key))
            return self.sequences_name[msg[sequence_key]]"""