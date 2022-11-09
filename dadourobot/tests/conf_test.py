import logging.config
import platform
import os

from dadourobot.config import RobotConfig


class TestSetup:

    def __init__(self):
        # check rapsberry
        if platform.machine() not in ('armv7l', 'armv6l'):
            path = "/home/dadou/Nextcloud/rosita/dadoutils/didier-dadoutils"
            os.chdir(path)
            print(os.path.join(path))

        logging.config.fileConfig('/home/didier/deploy/conf/logging-test.conf', disable_existing_loggers=False)
        logging.info("start logging")
