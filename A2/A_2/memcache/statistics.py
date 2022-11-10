# long-term statistics
used_size = 0
num_item_in_cache = 0
num_request_served = 0
num_GET_request_served = 0
num_hit = 0

prev_statistics_every_5s = []
statistics_10min = {
        'num_item_in_cache' : 0,
        'used_size' : 0,
        'num_request_served' : 0,
        'num_GET_request_served' : 0,
        'num_hit' : 0,
        'num_miss' : 0
    }