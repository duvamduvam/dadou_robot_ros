import logging


class KeysQueue:
    keys = {}

    def add_key(self, key):
        logging.info("key[" + str(len(self.keys)) + "] added : " + key)
        self.keys[len(self.keys)] = key
