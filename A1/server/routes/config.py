from server.libs.database import Database

DB = Database()

def get_config():
    return True, 200, dict(
        config=__serialize_config()
    )

def set_config(args):
    """
        1. save the config to database
        2. TODO: notify the config changes?
    """
    if args["clear"]:
        # TODO: send a request to clear the cache
        pass
    if args["policy"]:
        DB.set_config("policy", args["policy"])
    if args["capacity"]:
        DB.set_config("capacity", args["capacity"])
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