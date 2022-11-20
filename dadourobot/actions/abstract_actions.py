import logging

from dadou_utils.utils_static import KEY, KEYS, NAME


class ActionsAbstract:


    def __init__(self, json_manager, json_key=None):
        self.json_manager = json_manager
        self.sequences_key = {}
        self.sequences_name = {}
        if json_key : self.load_sequences(json_key)

    def load_sequences(self, json_key):
        sequences = self.json_manager.open_json(json_key)
        for seq in sequences:
            for key in seq[KEYS]:
                self.sequences_key[key] = seq
            self.sequences_name[seq[NAME]] = seq

    def get_sequence(self, msg, sequence_key):
        if msg and KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if msg and sequence_key in msg and msg[sequence_key] in self.sequences_name.keys():
            return self.sequences_name[msg[sequence_key]]

    """def get_sequence_from_input(self, msg, sequence_key):
        if not msg:
            return
        if KEY in msg and msg[KEY] in self.sequences_key.keys():
            return self.sequences_key[msg[KEY]]
        if sequence_key in msg and msg[sequence_key] in self.sequences_name.keys():
            logging.error("no {} in ".format(msg[sequence_key], sequence_key))
            return self.sequences_name[msg[sequence_key]]"""