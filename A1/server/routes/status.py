from server.libs.database import Database

DB = Database()


def status():
    """
        1. get status from database
    """
    status = DB.get_status()
    if None in status[0]: # empty status
        return True, 200, dict(
            status=[]
        )
    status = status[0]
    cache_nums_10mins = int(status[0])
    used_size_10mins = int(status[1])
    total_request_served_10mins = int(status[2])
    total_hit_10mins = int(status[3])
    hit_rate_10mins = str(round(status[4] / 120 * 100, 2)) + "%"
    miss_rate_10mins = str(round(status[5] / 120 * 100, 2)) + "%"

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
