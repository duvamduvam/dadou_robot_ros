import json
import logging
import os

from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from dadou_utils_ros.files.files_utils import FilesUtils
from dadou_utils_ros.utils_static import DB_DIRECTORY, SEQUENCES_DB, NAME, DURATION, KEYS, TYPES, FACES, ROBOT_LIGHTS, \
    LEFT_EYE, RIGHT_EYE, LEFT_ARM, RIGHT_ARM, NECK, SEQUENCES
from robot.robot_config import config

# Connexion à une base de données SQLite persistante
db_file = "{}{}".format(config[DB_DIRECTORY], config[SEQUENCES_DB])
engine = create_engine(f"sqlite:///{db_file}")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class SequencesDB2(Base):
    __tablename__ = SEQUENCES

    table_name = __tablename__

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    keys = Column(String, default=None)
    duration = Column(Integer)
    types = Column(String, default=None)
    faces = Column(String, default=None)
    lights = Column(String, default=None)
    robot_lights = Column(String, default=None)
    left_eye = Column(String, default=None)
    right_eye = Column(String, default=None)
    left_arm = Column(String, default=None)
    right_arm = Column(String, default=None)
    neck = Column(String, default=None)
    wheels = Column(String, default=None)
    audio = Column(String, default=None)
    audios = Column(String, default=None)
    audio_name = Column(String, default=None)
    audio_path = Column(String, default=None)
    loop = Column(Boolean, default=False)

    def drop(self):
        self.__table__.drop(engine)

    def create(self):
        self.__table__.create(engine)

