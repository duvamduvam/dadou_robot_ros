import logging
import os

from dadourobot.utils import Utils


class FileWatcher:
    keys = []
    file = os.getcwd() + '/../conf/test_key.txt'
    last_modified = os.path.getctime(file)

    def changed(self) -> bool:
        current_time = os.path.getctime(self.file)
        if current_time != self.last_modified:
            key = Utils.last_line(self.file)
            logging.info("key added : " + key)
            self.keys.append(key)
            return True
        return False

    def add_key_to_file(self, key):
        file = open(self.file, 'a')
        file.write("\n")
        file.write(key)
        file.close()

    def get_last_key(self) -> str:
        if len(self.keys) == 0:
            raise (IndexError, "keys list empty")
            return
        key = self.keys.pop()
        logging.info("pop key from file : "+key)
        return key
