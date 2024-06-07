import json
import logging
import logging.config
import os
import unittest
import random

from sqlobject import StringCol

from dadou_utils_ros.files.files_utils import FilesUtils
from dadou_utils_ros.logging_conf import LoggingConf
from dadou_utils_ros.utils_static import SEQUENCES_DIRECTORY, NAME, KEYS, DURATION, TYPES, FACES, ROBOT_LIGHTS, \
    LEFT_EYE, RIGHT_EYE, LEFT_ARM, RIGHT_ARM, NECK, LOGGING_TEST_FILE_NAME, SEQUENCES
from robot.db.db_manager2 import DBManager2
from robot.db.sequences_db import SequencesDB
from robot.db.sequences_db2 import SequencesDB2
from robot.db.db_manager import DBManager

from robot.robot_config import config


class MyTestCase(unittest.TestCase):
    print(config[LOGGING_TEST_FILE_NAME])
    logging.config.dictConfig(LoggingConf.get(config[LOGGING_TEST_FILE_NAME], "test db sequences"))

    def test_drop(self):

        logging.info("drop base")
        SequencesDB.dropTable()

    def test_import_json(self):

        logging.info("import json in db")

        if not SequencesDB.tableExists():
            SequencesDB.createTable()
        else:
            SequencesDB.dropTable()
            SequencesDB.createTable()

        sequences_files = FilesUtils.get_folder_files(config[SEQUENCES_DIRECTORY])
        for sequence_file in sequences_files:
            json_sequence = FilesUtils.open_json(sequence_file, 'r')
            logging.info(json_sequence)

            name = os.path.basename(sequence_file).replace(".json", "")
            db_fields = {NAME: name}
            if KEYS in json_sequence:
                db_fields[KEYS] = json_sequence[KEYS]
            if DURATION in json_sequence:
                db_fields[DURATION] = int(json_sequence[DURATION])  # Conversion en entier
            if TYPES in json_sequence:
                db_fields[TYPES] = json.dumps(json_sequence[TYPES])
            if FACES in json_sequence:
                db_fields[FACES] = json.dumps(json_sequence[FACES])
                logging.info(db_fields)
            if ROBOT_LIGHTS in json_sequence:
                db_fields[ROBOT_LIGHTS] = json.dumps(json_sequence[ROBOT_LIGHTS])
            if LEFT_EYE in json_sequence:
                db_fields[LEFT_EYE] = json.dumps(json_sequence[LEFT_EYE])
            if RIGHT_EYE in json_sequence:
                db_fields[RIGHT_EYE] = json.dumps(json_sequence[RIGHT_EYE])
            if LEFT_ARM in json_sequence:
                db_fields[LEFT_ARM] = json.dumps(json_sequence[LEFT_ARM])
            if RIGHT_ARM in json_sequence:
                db_fields[RIGHT_ARM] = json.dumps(json_sequence[RIGHT_ARM])
            if NECK in json_sequence:
                db_fields[NECK] = json.dumps(json_sequence[NECK])

            # Création de l'objet SequencesDB avec les champs conditionnels
            SequencesDB.insert(sequence_data=db_fields)

        #for seq in SequencesDB.select():
        #    seq.print()

    def test_import_json2(self):
        sequences_files = FilesUtils.get_folder_files(config[SEQUENCES_DIRECTORY])

        seq = SequencesDB

        #attributs = [attr for attr in dir(seq) if not callable(getattr(seq, attr)) and not attr.startswith("__")]
        #print(attributs)

        db_manager = DBManager2()
        db_manager.jsons_import(seq, sequences_files, create=True)

        row = db_manager.get_by_name(cls=seq, key=NAME, value="speak")

        logging.info(row)

    def test_import_json3(self):
        sequences_files = FilesUtils.get_folder_files(config[SEQUENCES_DIRECTORY])

        #seq = SequencesDB2()

        #seq.jsons_import(sequences_files, create=True)

        #SequencesDB2().drop()

        db_manager = DBManager()
        db_manager.jsons_import(SEQUENCES, sequences_files)


    def test_modules(self):
        print(globals())

    def test_create_db(self):
        if not SequencesDB.tableExists():
            SequencesDB.dropTable()
        fields = {NAME:StringCol(unique=True), TYPES:StringCol(default=None)}
        SequencesDB(fields)

        SequencesDB.createTable()
        #seq_db.dropTable()
        #seq_db.createTable()

    def test_get_sequence(self):
        n = NAME.lower()
        seq = SequencesDB.selectBy(n="little-neck")
        logging.info(seq)

    def test_raed_seq(self):
        for seq in SequencesDB.select():
            seq.print()



if __name__ == '__main__':
    unittest.main()
