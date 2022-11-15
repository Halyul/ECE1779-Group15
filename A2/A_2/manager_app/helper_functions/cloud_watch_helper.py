from datetime import datetime

import boto3


def get_one_min_data(cache_index: int, metric_name: str):
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
                    'Stat': ['Sum'],
                    'Unit': 'None'
                },
            },
        ],
        StartTime=datetime(2015, 1, 1),
        EndTime=datetime(2025, 1, 1),
        ScanBy='TimestampDescending',
    )
    result = []
    for point in response["Datapoints"]:
        result.append(point['Sum'])
    return result
