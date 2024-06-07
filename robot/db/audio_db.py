

from sqlobject import SQLObject, StringCol, IntCol
from sqlobject.sqlite import builder

from dadou_utils_ros.utils_static import DB_DIRECTORY, AUDIOS_DB
from robot.robot_config import config

# Connexion à une base de données SQLite persistante
db_file = "{}{}".format(config[DB_DIRECTORY], config[AUDIOS_DB])
connection = builder()(filename=db_file)


class AudioDB(SQLObject):
    _connection = connection

    name = StringCol()
    path = StringCol()
    length = IntCol()