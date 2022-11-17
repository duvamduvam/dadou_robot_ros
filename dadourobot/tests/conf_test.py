import logging.config
import platform
import os

from dadourobot.actions.neck import Neck
from dadourobot.config import RobotConfig
from dadourobot.files.robot_json_manager import RobotJsonManager
from dadourobot.robot_static import JSON_CONFIG


class TestSetup:

    def __init__(self):
        # check rapsberry
        if platform.machine() not in ('armv7l', 'armv6l'):
            path = "/home/dadou/Nextcloud/rosita/dadoutils/didier-dadoutils"
            os.chdir(path)
            print(os.path.join(path))

        logging.config.fileConfig('/home/didier/deploy/conf/logging-test.conf', disable_existing_loggers=False)
        logging.info("start logging")

        base_path = os.getcwd()
        robot_json_manager = RobotJsonManager('/home/didier/deploy/', 'json/', JSON_CONFIG)
        self.config = RobotConfig(robot_json_manager)

        self.neck = Neck(self.config)