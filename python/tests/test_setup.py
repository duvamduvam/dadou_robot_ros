import logging
import os


class TestSetup:

    def __init__(self):
        path = "/home/david/Nextcloud/rosita/python/didier-python"
        os.chdir(path)
        print(os.path.join(path))
        logging.config.fileConfig(fname='conf/logging-test.conf', disable_existing_loggers=False)
