from server.libs.database import Database

DB = Database()


def status():
    """
        TODO
        1. get status from database
    """
    status = DB.get_status()
    cache_nums_10mins = status[0]
    used_size_10mins = status[1]
    total_request_served_10mins = status[2]
    total_hit_10mins = status[3]
    hit_rate_10mins = status[4] / 120
    miss_rate_10mins = status[5] / 120

    return True, 200, dict(
        status=[
            {"name": "The number of items in cache", "value": cache_nums_10mins},
            {"name": "Cache memory used", "value": used_size_10mins},
            {"name": "The number of cache request", "value": total_request_served_10mins},
            {"name": "The number of hit", "value": total_hit_10mins},
            {"name": "Hit rate", "value": hit_rate_10mins},
            {"name": "Miss rate", "value": miss_rate_10mins},
        ]
    )
