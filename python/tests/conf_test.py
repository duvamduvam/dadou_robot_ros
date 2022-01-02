import logging
import platform
import os


class TestSetup:

    def __init__(self):
        #check rapsberry
        if platform.machine() not in ('armv7l', 'armv6l'):
            path = "/home/dadou/Nextcloud/rosita/python/didier-python"
            os.chdir(path)
            print(os.path.join(path))

        logging.config.fileConfig(fname='/home/pi/deploy/didier-python/conf/logging.conf', disable_existing_loggers=False)
