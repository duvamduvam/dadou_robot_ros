import sys
import time
import logging
from watchdog.observers import Observer

from watchdog.events import LoggingEventHandler

from dadou_utils.utils_static import INPUT_MESSAGE_FILE

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, "/home/didier/deploy/input_message/", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
