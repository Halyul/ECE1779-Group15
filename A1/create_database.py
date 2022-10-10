import mysql.connector
from server.config import Config

CONFIG = Config().fetch()["database"]
CONFIG_TABLE_NAME = CONFIG["table_names"]["config"]
KEY_IMAGE_TABLE_NAME = CONFIG["table_names"]["key_image"]
STATUS_TABLE_NAME = CONFIG["table_names"]["status"]

# Connect to the database
connection = mysql.connector.connect(
    host=CONFIG["host"],
    port=CONFIG["port"],
    user=CONFIG["user"],
    password=CONFIG["password"],
    database=CONFIG["name"]
)

# Create a cursor
cursor = connection.cursor()

# Create key_image table
cursor.execute("CREATE TABLE IF NOT EXISTS `{}` ("
                "`id` int NOT NULL AUTO_INCREMENT,"
                "`key` varchar(64) NOT NULL,"
                "`image` varchar(1024) NOT NULL,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci".format(KEY_IMAGE_TABLE_NAME))

# Create config table
cursor.execute("CREATE TABLE IF NOT EXISTS `{}` ("
                "`id` int NOT NULL AUTO_INCREMENT,"
                "`key` varchar(64) NOT NULL,"
                "`value` varchar(64) NOT NULL,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci".format(CONFIG_TABLE_NAME))

# Create status__new table
cursor.execute("CREATE TABLE IF NOT EXISTS `{}__new` ("
                "`id` int NOT NULL AUTO_INCREMENT,"
                "`cache_nums` int NOT NULL,"
                "`used_size` int NOT NULL,"
                "`total_request_served` int NOT NULL,"
                "`total_hit` int NOT NULL,"
                "`miss_rate` float NOT NULL DEFAULT 0,"
                "`hit_rate` float NOT NULL DEFAULT 0,"
                "PRIMARY KEY (`id`)"
                ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci".format(STATUS_TABLE_NAME))

# Try to rename status__new to status
try:
    cursor.execute("RENAME TABLE `{table_name}__new` TO `{table_name}`".format(table_name=STATUS_TABLE_NAME))
except mysql.connector.errors.ProgrammingError:
    # If status table already exists, rename status__new to status__new__1
    cursor.execute("RENAME TABLE `{table_name}` TO `{table_name}__old`, `{table_name}__new` TO `{table_name}`".format(table_name=STATUS_TABLE_NAME))
# Drop status__old table
cursor.execute("DROP TABLE IF EXISTS `{}__old`".format(STATUS_TABLE_NAME))

# Disconnect from the database
connection.close()