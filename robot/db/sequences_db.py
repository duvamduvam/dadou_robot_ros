import json
import logging
import os

from sqlobject import SQLObject, StringCol, IntCol, PickleCol, BoolCol
from sqlobject.dberrors import DuplicateEntryError
from sqlobject.sqlite import builder

from dadou_utils_ros.files.files_utils import FilesUtils
from dadou_utils_ros.utils_static import DB_DIRECTORY, SEQUENCES_DB, NAME, DURATION, KEYS, TYPES, FACES, ROBOT_LIGHTS, \
    LEFT_EYE, RIGHT_EYE, LEFT_ARM, RIGHT_ARM, NECK, SEQUENCES
from robot.robot_config import config

# Connexion à une base de données SQLite persistante
db_file = "{}{}".format(config[DB_DIRECTORY], config[SEQUENCES_DB])
connection = builder()(filename=db_file)


class SequencesDB(SQLObject):
    _connection = connection

    name = StringCol(unique=True)
    keys = StringCol(default=None)
    duration = IntCol()
    types = StringCol(default=None)
    faces = StringCol(default=None)

    lights = StringCol(default=None)
    robot_lights = StringCol(default=None)

    left_eye = StringCol(default=None)
    right_eye = StringCol(default=None)
    left_arm = StringCol(default=None)
    right_arm = StringCol(default=None)
    neck = StringCol(default=None)
    wheels = StringCol(default=None)

    audio = StringCol(default=None)
    audios = StringCol(default=None)
    audio_name = StringCol(default=None)
    audio_path = StringCol(default=None)

    loop = BoolCol(default=False)

    def print(self):
        # Log the values of all fields dynamically
        for field, col in self.sqlmeta.columns.items():
            print(f"{field}: {getattr(self, field)}")



    @staticmethod
    def json_import(file_path, create=False):

        if not SequencesDB.tableExists():
            SequencesDB.createTable()

        if create:
            SequencesDB.dropTable()
            SequencesDB.createTable()

        file = FilesUtils.open_json(file_path, 'r')
        logging.info(file)

        file[NAME] = os.path.basename(file_path).replace(".json", "")

        # Création de l'objet SequencesDB avec les champs conditionnels
        SequencesDB.insert(db_data=file)


    @staticmethod
    def jsons_import(json_files, create=False):
        logging.info("import json in db")

        for file_path in json_files:
            SequencesDB.json_import(file_path, create)
            create = False

    @staticmethod
    def insert(db_data):
        db_fields = {}
        for k, v in db_data.items():
            if isinstance(v, dict) or isinstance(v, list):
                db_fields[k] = json.dumps(v)
            else:
                db_fields[k] = v
        try:
            SequencesDB(**db_fields)
            logging.info(f"Inserted entry: {db_fields[NAME]}")
        except Exception as e:
            logging.error("Error adding {} => {}".format(db_fields, e))
