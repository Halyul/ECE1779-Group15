import datetime
import random
import threading

from app import config
from app.db_operations.configurations import get_capacity_in_mb_db
from app.db_operations.keys import get_image_size_db, get_least_recently_used_key_db, delete_key_db
from app.db_operations.statistics import store_stats_db


def delete_specific_cache(key):
    config.request_nums += 1
    config.memcache.pop(key)
    image_size = get_image_size_db(key)
    config.memcache_used_memory -= image_size


def release_cache_memory():
    replacement_policy = get_capacity_in_mb_db()[1]

    if replacement_policy == "Random Replacement":
        key_to_drop = random.randint(0, len(config.memcache))
    else:
        key_to_drop = get_least_recently_used_key_db()

    config.memcache.pop(key_to_drop)
    delete_key_db(key_to_drop)


def create_cache_statistics():
    threading.Timer(5.0, create_cache_statistics).start()
    timestamp = datetime.time()
    cache_nums = len(config.memcache)
    cache_size = config.memcache_used_memory
    req_nums = config.request_nums
    if req_nums == 0:
        miss_rate = None
        hit_rate = None
    else:
        miss_rate = config.miss_nums / req_nums
        hit_rate = 1 - miss_rate

    store_stats_db(timestamp, cache_nums, cache_size, req_nums, miss_rate, hit_rate)
    print("Stats stored")
