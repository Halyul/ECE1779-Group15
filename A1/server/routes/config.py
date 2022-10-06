from server.libs.database import Database
import requests
import json

DB = Database()
memcache_url = "http://127.0.0.1:5001" # TODO: may need a better place

config_base = {
    "policy": "rr",
    "capacity": 100,
}

def get_config():
    """
        1. get config from database
    """
    config = DB.get_config()
    print(config)
    return True, 200, dict(
        config=config_base
    )

def set_config(args):
    """
        1. save the config to database
        2. notify the config changes?
    """
    # TODO: do we need to handle the case that http responce from memcache returns an error?
    response = ""
    if args["clear"]:
        # send a request to clear the cache
        config_base.clear()
        response = json.loads(requests.delete(memcache_url + "/api/cache"))
    if args["policy"]:
        DB.set_config("policy", args["policy"])
        config_base["policy"] = args["policy"]
        response = json.loads(requests.get(memcache_url + "/api/cache/config"))
    if args["capacity"]:
        DB.set_config("capacity", args["capacity"])
        config_base["capacity"] = args["capacity"]
        response = json.loads(requests.get(memcache_url + "/api/cache/config"))
    return True, 200, dict(
        config=config_base
    )
