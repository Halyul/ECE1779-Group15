# long-term statistics
used_size = 0
num_item_in_cache = 0
num_request_served = 0
num_GET_request_served = 0
# this num_hit value may change - master node will take the total num_hit values, slave nodes will constantly set to 0
num_hit = 0

# this num_hit value is used for couldwatch, so will only increase no matter this is a master or slave node
num_hit_cloudwatch = 0

prev_statistics_every_5s = []
statistics_10min = {
        'num_item_in_cache' : 0,
        'used_size' : 0,
        'num_request_served' : 0,
        'num_GET_request_served' : 0,
        'num_hit' : 0,
        'num_miss' : 0
    }