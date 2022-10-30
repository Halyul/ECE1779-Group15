import boto3

def my_put_metric_data(CacheIndex:int, MetricName:str, MetricValue:float):
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': MetricName,
                'Dimensions': [
                    {
                        'Name': 'CacheIndex',
                        'Value': 'Cache #' + str(CacheIndex)
                    },
                ],
                'Unit': 'None',
                'Value': MetricValue
            },
        ],
        Namespace='ECE1779 Memcache Statistics'
    )
    return