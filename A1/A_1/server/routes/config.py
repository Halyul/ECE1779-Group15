from server.config import Config
from server.libs.database import Database
from server.libs.thread_task import ThreadTask
import requests

CONFIG = Config().fetch()
CACHE_URL = "http://{host}:{port}".format(**CONFIG["cache"])
CONFIG_TABLE_NAME = CONFIG["database"]["table_names"]["config"]

# speical accommodations for the cache server
ThreadTask(
        requests.get,
        kwargs=dict(
            url = CACHE_URL + "/api/cache/config",
        )
    ).start()

def get_config():
    return True, 200, dict(
        config=__serialize_config()
    )

def set_config(args):
    """
        1. save the config to database
        2. notify the config changes
    """
    database = Database()
    database.lock(table=CONFIG_TABLE_NAME)
    if "clear_cache" in args and args["clear_cache"]:
        ThreadTask(
            requests.delete, 
            kwargs=dict(
                url = CACHE_URL + "/api/cache",
            )
        ).start()
    if "policy" in args:
        database.set_config("policy", args["policy"])
    if "capacity" in args:
        if 0 <= args["capacity"] <= 2048:
            database.set_config("capacity", args["capacity"])
    ThreadTask(
        requests.get,
        kwargs=dict(
            url = CACHE_URL + "/api/cache/config",
        )
    ).start()
    database.unlock()
    return True, 200, dict(
        config=__serialize_config()
    )

def __serialize_config():
    database = Database()
    database.lock(table=CONFIG_TABLE_NAME)
    config_entries = database.get_config()
    database.unlock()
    config = {
        "policy": None,
        "capacity": None
    }
    for e in config_entries:
        if e[0] == "policy":
            config["policy"] = e[1]
        elif e[0] == "capacity":
            config["capacity"] = e[1]
    return config