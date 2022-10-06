from server.libs.database import Database

DB = Database()

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
    if args["clear"]:
        # send a request to clear the cache
        config_base.clear()
    if args["policy"]:
        DB.set_config("policy", args["policy"])
        config_base["policy"] = args["policy"]
    if args["capacity"]:
        DB.set_config("capacity", args["capacity"])
        config_base["capacity"] = args["capacity"]
    return True, 200, dict(
        config=config_base
    )
