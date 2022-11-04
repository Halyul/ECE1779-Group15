import mysql.connector
from server.config import Config

CONFIG = Config().fetch()["database"]
KEY_IMAGE_TABLE_NAME = CONFIG["table_names"]["key_image"]

# Connect to the database
connection = mysql.connector.connect(
    host=CONFIG["host"],
    port=CONFIG["port"],
    user=CONFIG["user"],
    password=CONFIG["password"],
)

# Create a cursor
cursor = connection.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(CONFIG["name"]))

# Use database
cursor.execute("USE {}".format(CONFIG["name"]))

# Create key_image table
cursor.execute("CREATE TABLE IF NOT EXISTS `{}` ("
                "`id` int NOT NULL AUTO_INCREMENT,"
                "`key` varchar(64) NOT NULL,"
                "`image` varchar(1024) NOT NULL,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci".format(KEY_IMAGE_TABLE_NAME))

# Disconnect from the database
connection.close()
