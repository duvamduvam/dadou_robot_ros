import json
import logging
import os

from sqlobject import SQLObject

from dadou_utils_ros.files.files_utils import FilesUtils
from dadou_utils_ros.utils_static import NAME


class AbstractDB(SQLObject):

    def print(self):
        # Log the values of all fields dynamically
        for field, col in self.sqlmeta.columns.items():
            print(f"{field}: {getattr(self, field)}")

    def json_import(self, file_path, create=False):

        if not self.tableExists():
            self.createTable()

        if create:
            self.dropTable()
            self.createTable()

        file = FilesUtils.open_json(file_path, 'r')
        logging.info(file)

        file[NAME] = os.path.basename(file_path).replace(".json", "")

        # Création de l'objet SequencesDB avec les champs conditionnels
        self.insert(db_data=file)

    def jsons_import(self, json_files, create=False):
        logging.info("import json in db")

        for file_path in json_files:
            self.json_import(file_path, create)
            create = False

    def insert(self, db_data):
        db_fields = {}
        for k, v in db_data.items():
            if isinstance(v, dict) or isinstance(v, list):
                db_fields[k] = json.dumps(v)
            else:
                db_fields[k] = v
        try:
            self.insert(**db_fields)
            #self(**db_fields)
            logging.info(f"Inserted entry: {db_fields[NAME]}")
        except Exception as e:
            logging.error("Error adding {} => {}".format(db_fields, e))
