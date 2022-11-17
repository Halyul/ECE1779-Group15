from datetime import datetime, timedelta

import boto3
from pytz import timezone

from auto_scaler.libs.cloudwatch_func import my_get_metric_data
from manager_app import variables


def get_one_min_data():
    total_num_item_in_cache = 0
    total_used_size = 0
    total_num_request_served = 0
    total_num_hit = 0
    total_num_get_request_served = 0

    pool_size = len(variables.pool_node_id_list)
    for i in range(pool_size):
        num_item_in_cache = my_get_metric_data(i, 'number of keys added', 'Maximum')
        if num_item_in_cache != []:
            total_num_item_in_cache += num_item_in_cache[0]

        used_size = my_get_metric_data(i, 'capacity used', 'Maximum')
        if used_size != []:
            total_used_size += used_size[0]

        num_request_served = my_get_metric_data(i, 'request served', 'Maximum')
        if num_request_served != []:
            total_num_request_served += num_request_served[0]

        num_hit = my_get_metric_data(i, 'number of hit', 'Maximum')
        if num_hit != []:
            total_num_hit += num_hit[0]

        num_get_request_served = my_get_metric_data(i, 'GET request served', 'Maximum')
        if num_get_request_served != []:
            total_num_get_request_served += num_get_request_served[0]

    if total_num_get_request_served == 0:
        hit_rate = 0
        miss_rate = 0
    else:
        hit_rate = float(total_num_hit) / total_num_get_request_served * 100
        miss_rate = 100 - hit_rate

    total_used_size = float(total_used_size) / (1024 * 1024)

    variables.miss_rate.append(miss_rate)
    variables.hit_rate.append(hit_rate)
    variables.cache_item_num.append(total_num_item_in_cache)
    variables.cache_total_size.append(total_used_size)
    variables.request_served_num.append(total_num_request_served)

    return
