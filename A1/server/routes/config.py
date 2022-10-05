
config_base = dict(
            policy="rr",
            capacity=100
        )

def get_config():
    return True, 200, dict(
        config=config_base
    )

def set_config(args):
    if args["clear"]:
        config_base.clear()
    if args["policy"]:
        config_base["policy"] = args["policy"]
    if args["capacity"]:
        config_base["capacity"] = args["capacity"]
    return True, 200, dict(
        config=config_base
    )
