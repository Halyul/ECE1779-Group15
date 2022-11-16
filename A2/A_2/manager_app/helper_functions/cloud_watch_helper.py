from datetime import datetime, timedelta

import boto3

from manager_app import variables


def my_get_metric_data(cache_index: int, metric_name: str):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'stats_per_one_min',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'ECE1779 Memcache Statistics',
                        'MetricName': metric_name,
                        'Dimensions': [
                            {
                                'Name': 'CacheIndex',
                                'Value': 'Cache #' + str(cache_index)
                            },
                        ]
                    },
                    'Period': 60,
                    'Stat': 'Sum',
                    'Unit': 'None'
                },
            },
        ],
        StartTime=datetime.now() - timedelta(minutes=1),
        EndTime=datetime.now(),
        ScanBy='TimestampDescending',
    )
    value = 0
    results = response["MetricDataResults"]
    if not results:
        return 0
    for result in results:
        if not result['Values']:
            value += sum(result['Values'])
    return value


def get_one_min_data():
    num_item_in_cache = 0
    used_size = 0
    num_request_served = 0
    num_hit = 0
    num_get_request_served = 0

    pool_size = len(variables.pool_node_id_list)
    for i in range(pool_size):
        num_item_in_cache += my_get_metric_data(i, 'number of keys added')
        used_size += my_get_metric_data(i, 'capacity used')
        num_request_served += my_get_metric_data(i, 'request served')
        num_hit += my_get_metric_data(i, 'num_hit')
        num_get_request_served += my_get_metric_data(i, 'GET request served')

    if num_get_request_served == 0:
        hit_rate = 0
        miss_rate = 0
    else:
        hit_rate = float(num_hit) / num_get_request_served * 100
        miss_rate = 100 - hit_rate

    variables.miss_rate.append(miss_rate)
    variables.hit_rate.append(hit_rate)
    variables.cache_item_num.append(num_item_in_cache)
    variables.cache_total_size.append(used_size)
    variables.request_served_num.append(num_request_served)

    return
