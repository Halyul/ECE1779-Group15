from enum import Enum
import mysql.connector
from server.config import Config

CONFIG = Config().fetch()["database"]
KEY_IMAGE_TABLE_NAME = CONFIG["table_names"]["key_image"]

class Mode(Enum):
    WRITE = 1
    READ = 0

class Database:

    def __init__(self):
        self.host = CONFIG["host"]
        self.port = CONFIG["port"]
        self.user = CONFIG["user"]
        self.password = CONFIG["password"]
        self.database = CONFIG["name"]
        self.connection = None
        self.cursor = None
        self.__connect()

    def __connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def create_key_image_pair(self, key, image):
        self.__execute(
            "INSERT INTO `{table_name}` (`key`, `image`) VALUES (%s, %s)".format(table_name=KEY_IMAGE_TABLE_NAME),
            (key, image))

    def get_key_image_pair(self, key):
        return self.__fetch_one(
            "SELECT `image` FROM `{table_name}` WHERE `key` = %s".format(table_name=KEY_IMAGE_TABLE_NAME), (key,))

    def get_keys(self):
        return self.__fetch("SELECT `key` FROM {table_name}".format(table_name=KEY_IMAGE_TABLE_NAME))

    def clear_keys(self):
        self.__execute("DELETE FROM {table_name}".format(table_name=KEY_IMAGE_TABLE_NAME))
    
    def lock(self, table, mode=Mode.WRITE):
        self.__execute("LOCK TABLES `{table_name}` {mode}".format(table_name=table, mode="WRITE" if mode == Mode.WRITE else "READ"))
    
    def unlock(self):
        self.__execute("UNLOCK TABLES")

    def __disconnect(self):
        self.connection.close()

    def __execute(self, query, args=None):
        self.cursor.execute(query, args)
        self.connection.commit()

    def __fetch(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def __fetch_one(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()

    def __enter__(self):
        self.__connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__disconnect()
