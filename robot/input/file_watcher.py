#!/usr/bin/python
import json
import logging
import os
from json import JSONDecodeError

from watchdog.events import FileSystemEventHandler

from dadou_utils_ros.static_value import StaticValue
from dadou_utils_ros.utils_static import INPUT_MESSAGE_FILE, NEW_DATA



class FileWatcher(FileSystemEventHandler):

    new_data = False
    msg_timeout = 1000
    msg_last_time = 0
    last_msg = {}

    def on_modified(self, event):
        new_msg = self.read_msg()
        logging.info(os.path.getctime(INPUT_MESSAGE_FILE))
        if new_msg and not self.last_msg == new_msg:
            #self.msg_last_time = TimeUtils.current_milli_time()
            StaticValue.set(NEW_DATA, True)
            logging.debug("new msg {}".format(new_msg))

    @staticmethod
    def read_msg():
        with open(INPUT_MESSAGE_FILE, 'r') as j:
            try:
                return json.loads(j.read())
            except JSONDecodeError:
                logging.debug("{} wrong format {}".format(INPUT_MESSAGE_FILE, j))

    def get_msg(self):

        msg_from_file = self.read_msg()
        new_msg = {}
        if msg_from_file:
            for key in msg_from_file.keys():
                if isinstance(msg_from_file[key], list):
                    if key in self.last_msg:
                        if not isinstance(self.last_msg[key], list):
                            new_msg[key] = msg_from_file[key][1]
                        else:
                            if not self.last_msg[key][0] == msg_from_file[key][0]:
                                new_msg[key] = msg_from_file[key][1]
                    else:
                        new_msg[key] = msg_from_file[key][1]
                else:
                    new_msg[key] = msg_from_file[key]
            self.last_msg = msg_from_file
        else:
            logging.debug("msg from file empty")
        return new_msg


"""if __name__ == "__main__":
    event_handler = FileWatcher()
    observer = Observer()
    observer.schedule(event_handler, path='/data/', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
"""
