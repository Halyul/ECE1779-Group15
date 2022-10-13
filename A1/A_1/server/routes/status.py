from server.libs.database import Database

def status():
    """
        1. get status from database
    """
    status = Database().get_status()
    if None in status: # empty status
        return True, 200, dict(
            status=[]
        )
    cache_nums_10mins = int(status[0])
    used_size_10mins = str(round(int(status[1]) / (1024 * 1024), 2)) + " MB"
    total_request_served_10mins = int(status[2])
    total_GET_request_served_10mins = int(status[3])
    total_hit_10mins = int(status[4])
    try:
        hit_rate_10mins = round(total_hit_10mins / total_GET_request_served_10mins * 100, 2)
        miss_rate_10mins = str(100 - hit_rate_10mins) + "%"
        hit_rate_10mins = str(hit_rate_10mins) + "%"
    except ZeroDivisionError:
        hit_rate_10mins = "0%"
        miss_rate_10mins = "0%"

    utilization = str(round(status[5], 2) * 100) + "%"

    return True, 200, dict(
        status=[
            {"name": "The number of items in cache", "value": cache_nums_10mins},
            {"name": "Cache memory used", "value": used_size_10mins},
            {"name": "The number of cache request", "value": total_request_served_10mins},
            {"name": "The number of cache GET request", "value": total_GET_request_served_10mins},
            {"name": "The number of hit", "value": total_hit_10mins},
            {"name": "Hit rate", "value": hit_rate_10mins},
            {"name": "Miss rate", "value": miss_rate_10mins},
            {"name": "Utilization", "value": utilization},
        ]
    )
