import mysql.connector
from server.config import Config

CONFIG = Config().fetch()["database"]
CONFIG_TABLE_NAME = CONFIG["table_names"]["config"]
KEY_IMAGE_TABLE_NAME = CONFIG["table_names"]["key_image"]
STATUS_TABLE_NAME = CONFIG["table_names"]["status"]

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
        self.__create_default_config()

    def __connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def __create_default_config(self):
        if not self.get_config():
            self.__execute(
                "INSERT INTO `{table_name}` (`key`, `value`) VALUES (%s, %s)".format(table_name=CONFIG_TABLE_NAME),
                ("policy", "rr"))
            self.__execute(
                "INSERT INTO `{table_name}` (`key`, `value`) VALUES (%s, %s)".format(table_name=CONFIG_TABLE_NAME),
                ("capacity", "100"))

    def get_config(self):
        return self.__fetch("SELECT `key`, `value` FROM {}".format(CONFIG_TABLE_NAME))

    def set_config(self, key, value):
        self.__execute("UPDATE `{table_name}` SET `value` = %s WHERE `key` = %s".format(table_name=CONFIG_TABLE_NAME),
                       (value, str(key)))

    def get_status(self):
        status_base = self.__fetch_one("SELECT SUM(`cache_nums`), SUM(`used_size`), SUM(`total_request_served`), SUM(`total_GET_request_served`), "
                            "SUM(`total_hit`), SUM(`hit_rate`), SUM(`miss_rate`) "
                            "FROM (SELECT * FROM {table_name} ORDER BY `id` DESC LIMIT 120) as `s*`".format(table_name=STATUS_TABLE_NAME))
        utl = self.__fetch_one("SELECT `utilization` FROM {table_name} ORDER BY `id` DESC LIMIT 1".format(table_name=STATUS_TABLE_NAME))
        return status_base + utl

    def create_key_image_pair(self, key, image):
        self.__execute(
            "INSERT INTO `{table_name}` (`key`, `image`) VALUES (%s, %s)".format(table_name=KEY_IMAGE_TABLE_NAME),
            (key, image))

    def get_key_image_pair(self, key):
        return self.__fetch_one(
            "SELECT `image` FROM `{table_name}` WHERE `key` = %s".format(table_name=KEY_IMAGE_TABLE_NAME), (key,))

    def get_keys(self):
        return self.__fetch("SELECT `key` FROM {table_name}".format(table_name=KEY_IMAGE_TABLE_NAME))

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
