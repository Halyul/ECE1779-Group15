import boto3
import pytz
from datetime import datetime, timedelta

def my_get_metric_data(CacheIndex:int, MetricName:str, stat:str):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "result_" + MetricName.replace(" ", "_"),
                "MetricStat": {
                    "Metric": {
                        "Namespace": "ECE1779 Memcache Statistics",
                        "MetricName": MetricName,
                        "Dimensions": [{"Name": "CacheIndex", "Value": 'Cache #' + str(CacheIndex)}],
                    },
                    "Period": 60,
                    "Stat": stat,
                },
            },
        ],
        # using Standard resolution which is 60s due to the free trial
        StartTime=datetime.now(tz=pytz.utc) - timedelta(seconds=60),
        EndTime=datetime.now(tz=pytz.utc),
    )
    return response['MetricDataResults'][0]['Values'] 

def get_num_GET_request_served(CacheIndex:int):
    # using 'Maximum' since num_GET_requesst_served do not decrease by itself
    # the only spical case is a node is distroyed and then created again within 1min, but this is
    # not realistic since auto_scaler do pool size adjustment 1 time each minute
    return my_get_metric_data(CacheIndex, 'GET request served', 'Maximum')

def get_num_hit(CacheIndex:int):
    return my_get_metric_data(CacheIndex, 'number of hit', 'Maximum')