import random
import threading

from memcache_Shawn.memcache.app import config
from memcache_Shawn.memcache.app.db_operations.statistics import store_stats_db


def release_cache_memory():
    if config.memcache_config_replacement_policy == "rr":
        key_to_drop = random.randint(0, len(config.memcache))
    else:
        key_to_drop = config.memcache_keys_ordered[0]
    image_size = config.memcache.pop(key_to_drop)
    config.memcache_used_memory -= image_size


def create_cache_statistics():
    threading.Timer(5, create_cache_statistics).start()
    cache_nums = len(config.memcache)
    cache_used_size = config.memcache_used_memory
    req_nums = config.memcache_request_nums
    total_hit = config.memcache_total_hit
    if req_nums == 0:
        hit_rate = 0
        miss_rate = 0
    else:
        hit_rate = total_hit / req_nums
        miss_rate = 1 - hit_rate

    store_stats_db(cache_nums, cache_used_size, req_nums, total_hit, hit_rate, miss_rate)
