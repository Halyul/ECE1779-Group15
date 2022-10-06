import mysql.connector
from server.config import Config

CONFIG = Config().fetch()["database"]

TABLES = {
    "config": {
        "fields": {
            "policy": "text",
            "capacity": "numeric",
        }
    },
    "status": {
        "fields": {
            "num_item_in_cache": "numeric",
            "used_size": "numeric",
            "total_request_served": "numeric",
            "total_hit": "numeric",
            "miss_rate": "numeric",
            "hit_rate": "numeric",
        }
    },
    "key_image": {
        "fields":{
            "key": "text",
            "image": "text",
        }
    }
}

class Database:

    def __init__(self):
        self.host = CONFIG["host"]
        self.user = CONFIG["user"]
        self.password = CONFIG["password"]
        self.database = CONFIG["database"]
        self.connection = None
        self.cursor = None
        self.__connect()
        self.__create_table()

    def __connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
    
    def __create_table(self, schema):
        self.__execute(f"CREATE TABLE IF NOT EXISTS key_images ({schema})")
    
    def get_config(self):
        return self.__fetch_one("SELECT * FROM config")

    def set_config(self, key, value):
        self.__execute("UPDATE config SET value = %s WHERE key = %s", (value, key))

    def get_status(self):
        return self.__fetch_one("SELECT * FROM status")

    def create_key_image_pair(self, key, image):
        self.__execute("INSERT INTO key_image_pairs (key, image) VALUES (%s, %s)", (key, image))
    
    def get_key_image_pair(self, key):
        return self.__fetch_one("SELECT * FROM key_image_pairs WHERE key = %s", (key,))
    
    def get_keys(self):
        return self.__fetch("SELECT * FROM keys")

    def disconnect(self):
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
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()