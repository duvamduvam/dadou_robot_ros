import logging
import os

import sqlalchemy as db

from sqlalchemy import Column as sqla_Column

from sqlalchemy import Integer as sqla_Integer
from sqlalchemy import String as sqla_String

from dadou_utils_ros.files.files_utils import FilesUtils
from dadou_utils_ros.utils_static import NAME
from robot.db.sequences_db2 import SequencesDB2


class DBManager:

    tables = [SequencesDB2]

    def create(self, table, fields):
        table = self.get_table(table)
        row = table(fields)
        row.session.add(row)
        row.session.commit()

    def get_by_name(self, table, value):
        table = self.get_table(table)
        return table.session.query(table).filter_by(name=value).first()

    def get_table(self, name):
        for table in self.tables:
            if table.table_name == name:
                return table

    def json_import(self, table, file_path, create=False):

        file = FilesUtils.open_json(file_path, 'r')
        logging.info(file)

        file[NAME] = os.path.basename(file_path).replace(".json", "")

        # Création de l'objet SequencesDB avec les champs conditionnels
        self.create(table, file)

    def jsons_import(self, table, json_files, create=False):
        logging.info("import json in db")

        for file_path in json_files:
            self.json_import(table, file_path, create)
            create = False
