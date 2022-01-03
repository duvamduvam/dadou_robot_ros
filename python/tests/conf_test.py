import logging.config
import platform
import os


class TestSetup:

    def __init__(self):
        #check rapsberry
        if platform.machine() not in ('armv7l', 'armv6l'):
            path = "/home/dadou/Nextcloud/rosita/python/didier-python"
            os.chdir(path)
            print(os.path.join(path))

        logging.config.fileConfig(fname='conf/logging-test.conf', disable_existing_loggers=False)
        logging.info("start logging")
