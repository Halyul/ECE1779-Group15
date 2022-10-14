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

    def __connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def get_config(self):
        return self.__fetch("SELECT `key`, `value` FROM {}".format(CONFIG_TABLE_NAME))

    def set_config(self, key, value):
        self.__execute("UPDATE `{table_name}` SET `value` = %s WHERE `key` = %s".format(table_name=CONFIG_TABLE_NAME),
                       (value, str(key)))

    def get_status(self):
        data = self.__fetch("SELECT `cache_nums`, `used_size`, `total_request_served`, `total_GET_request_served`, `total_hit`, `utilization` "
                                "FROM {table_name} ORDER BY `id` DESC LIMIT 120;".format(table_name=STATUS_TABLE_NAME))
        (num_key_added_end, used_size_end, request_served_end, GET_request_served_end, num_hit_end, utl) = data[0]
        (num_key_added_start, used_size_start, request_served_start, GET_request_served_start, num_hit_start, unused) = data[-1]
        
        status_base = (num_key_added_end - num_key_added_start, \
                       used_size_end - used_size_start, \
                       request_served_end - request_served_start, \
                       GET_request_served_end - GET_request_served_start, \
                       num_hit_end - num_hit_start, \
                       utl)
        return status_base

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
