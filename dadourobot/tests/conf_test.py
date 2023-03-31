import platform
import os

from dadou_utils.utils_static import RPI_TYPE


class TestSetup:

    def __init__(self):
        # check rapsberry
        if platform.machine() not in RPI_TYPE:
            path = "/home/dadou/Nextcloud/rosita/dadoutils/didier-dadoutils"
            os.chdir(path)
            print(os.path.join(path))

        #self.left_arm = robot_factory.left_arm
        #self.right_arm = robot_factory.right_arm
        #self.neck = robot_factory.neck
        #self.wheel = robot_factory.wheel

