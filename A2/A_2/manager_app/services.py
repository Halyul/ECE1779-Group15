import boto3
import requests
from flask import request

from manager_app.ec2_helper_functions import ec2_get_instance, ec2_create, ec2_destroy, ec2_destroy_all
from manager_app.responses import success_response, failed_response
from manager_app.s3_helper_functions import s3_list, s3_clear
from server.config import Config
from manager_app import data
from db_operations import get_stats_from_db

CONFIG = Config().fetch()
AUTO_SCALAR_URL = "http://{host}:{port}".format(**CONFIG["auto_scalar"])
CACHE_URL = "http://{host}:{port}".format(**CONFIG["cache"])


def get_node_num():
    instances = ec2_get_instance()
    node_num = instances.size()
    return success_response(node_num)


def get_30_min_data():
    if data.size >= 30:
        data.pop(0)
    data.append(get_stats_from_db())


def set_cache_configurations():
    response = requests.post(CACHE_URL + "/api/cache/config")
    content = response["content"]
    return success_response(content)


def increase_pool_size():
    instances = ec2_get_instance()
    if instances.size() == 8:
        return failed_response(400, "The size of memcache pool has been reached to maximum")
    else:
        ec2_create()
        return success_response("Memcache pool size increases")


def decrease_pool_size():
    instances = ec2_get_instance()
    if not instances:
        return 400, "The size of memcache pool has been reached to minimum"
    else:
        instance = instances[0]
        ec2_destroy(instance.id)
        return success_response("Memcache pool size decreases")


def set_auto_scaler_parameters():
    max_miss_rate_threshold = request.form.get('max_miss_rate_threshold')
    min_miss_rate_threshold = request.form.get('min_miss_rate_threshold')
    ratio_expand_pool = request.form.get('ratio_expand_pool')
    ratio_shrink_pool = request.form.get('ratio_shrink_pool')

    response = requests.post(AUTO_SCALAR_URL + "/api/scaler/config",
                             data={'max_miss_rate_threshold': max_miss_rate_threshold,
                                   'min_miss_rate_threshold': min_miss_rate_threshold,
                                   'ratio_expand_pool': ratio_expand_pool,
                                   'ratio_shrink_pool': ratio_shrink_pool})
    content = response["content"]
    return success_response(content)


def clear_all_cache():
    # Make it for all ec2 instances
    response = requests.delete(CACHE_URL + "/api/cache")
    content = response["content"]
    return success_response(content)


def clear_all_data():
    # EC2
    ec2_destroy_all()

    # S3
    buckets = s3_list()
    s3_clear(buckets[0])

    # RDS
