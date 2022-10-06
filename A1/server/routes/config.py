from server.config import Config
from server.libs.database import Database
import requests
import json

DB = Database()
CONFIG = Config().fetch()
CACHE_URL = "http://{host}:{port}".format(**CONFIG["cache"])

def get_config():
    return True, 200, dict(
        config=__serialize_config()
    )

def set_config(args):
    """
        1. save the config to database
        2. TODO: notify the config changes?
    """
    # TODO: do we need to handle the case that http responce from memcache returns an error?
    response = ""
    if args["clear"]:
        response = json.loads(requests.delete(CACHE_URL + "/api/cache"))
    if args["policy"]:
        DB.set_config("policy", args["policy"])
    if args["capacity"]:
        DB.set_config("capacity", args["capacity"])
    response = json.loads(requests.get(CACHE_URL + "/api/cache/config"))
    return True, 200, dict(
        config=__serialize_config()
    )

def __serialize_config():
    config_entries = DB.get_config()
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