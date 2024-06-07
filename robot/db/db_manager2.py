import json
import logging
import os

import sqlalchemy as db

from sqlalchemy import Column as sqla_Column

from sqlalchemy import Integer as sqla_Integer
from sqlalchemy import String as sqla_String

from dadou_utils_ros.files.files_utils import FilesUtils
from dadou_utils_ros.utils_static import NAME
from robot.db.sequences_db2 import SequencesDB2


class DBManager2:

    tables = [SequencesDB2]

    def create(self, table, fields):
        table = self.get_table(table)
        row = table(fields)
        row.session.add(row)
        row.session.commit()

    def get_by_name(self, cls, value):
        res = cls.select(cls.q.name == value)
        if len(res) > 0:
            return res[0]

    def get_table(self, name):
        for table in self.tables:
            if table.table_name == name:
                return table

    @staticmethod
    def jsons_import(cls, json_files, create=False):
        logging.info("import json in db")

        for file_path in json_files:
            cls.json_import(file_path, create)
            create = False

    @staticmethod
    def insert(cls, db_data):
        db_fields = {}
        for k, v in db_data.items():
            if isinstance(v, dict) or isinstance(v, list):
                db_fields[k] = json.dumps(v)
            else:
                db_fields[k] = v
        try:
            cls(**db_fields)
            logging.info(f"Inserted entry: {db_fields[NAME]}")
        except Exception as e:
            logging.error("Error adding {} => {}".format(db_fields, e))