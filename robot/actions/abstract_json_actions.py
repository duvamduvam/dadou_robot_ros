import logging
import os
import random

from dadou_utils.files.files_utils import FilesUtils
from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.utils_static import KEY, KEYS, NAME, LOOP, RANDOM_ANIMATION_LOW, RANDOM_ANIMATION_HIGH, \
    LOOP_DURATION, \
    DURATION, BASE_PATH, TYPE, TYPES


class AbstractJsonActions:

    global_duration = 0
    start_global_lime = 0
    loop = False

    def __init__(self, config, json_manager, json_file=None, action_type=None, sequence_dir=None):
        self.config = config
        self.sequences_key = {}
        self.sequences_name = {}
        self.json_file = json_file
        if not sequence_dir:
            self.load_keys_and_names_sequences(json_manager)
        else:
            self.load_multi_files_sequences(sequence_dir)
        self.action_type = action_type
        self.msg_time = 0

    def load_keys_and_names_sequences(self, json_manager):
        sequences = json_manager.open_json(self.json_file)
        for seq_key in sequences:
            if KEYS in sequences[seq_key].keys():
                for key in sequences[seq_key][KEYS]:
                    self.sequences_key[key] = sequences[seq_key]
            self.sequences_name[seq_key] = sequences[seq_key]
            self.sequences_name[seq_key][NAME] = seq_key

    def load_multi_files_sequences(self, sequence_dir):
        sequences_files = FilesUtils.get_folder_files(sequence_dir)
        for sequence_file in sequences_files:
            json_sequence = FilesUtils.open_json(sequence_file, 'r')
            json_sequence[NAME] = os.path.basename(sequence_file).replace(".json", "")
            self.sequences_key[json_sequence[KEYS]] = json_sequence
            self.sequences_name[json_sequence[NAME]] = json_sequence

    def get_sequence(self, msg, animation_loop):

        if not msg or (KEY not in msg and self.action_type not in msg):
            return

        sequence = None
        if self.action_type in msg and msg[self.action_type] in self.sequences_name:
            sequence = self.sequences_name[msg[self.action_type]]
        elif KEY in msg and msg[KEY] in self.sequences_key:
            sequence = self.sequences_key[msg[KEY]]

        if sequence:
            if animation_loop and DURATION in msg.keys():
                self.global_duration = msg[DURATION]
                self.start_global_lime = TimeUtils.current_milli_time()
            return sequence
        else:
           logging.debug("no sequence with key {}".format(self.json_file))

    def get_random_sequence(self, type):
        random_sequences = []
        for sequence in self.sequences_name:
            if TYPES in self.sequences_name[sequence] and type in self.sequences_name[sequence][TYPES]:
                random_sequences.append(sequence)
        if len(random_sequences) > 0:
            rand_sequence = random_sequences[random.randint(0, len(random_sequences)-1)]
            logging.info("random sequence: {}".format(rand_sequence))
            return rand_sequence

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