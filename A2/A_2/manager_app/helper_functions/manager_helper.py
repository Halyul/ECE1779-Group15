import logging
import threading
import time

import requests

from manager_app import variables, config
from manager_app.helper_functions.cloud_watch_helper import get_one_min_data
from manager_app.helper_functions.ec2_helper import ec2_create, ec2_destroy, ec2_get_instance_ip
from manager_app.helper_functions.ssh_helper import run_cache_update_status


def generate_node_ip_list():
    ip_list = []
    for node_id in variables.pool_node_id_list:
        ip_list.append(ec2_get_instance_ip(node_id))
    return ip_list


def increase_pool_size_manual():
    """
    1. Create ec2 instance
    2. Update local node_list
    3. Run instance2 on new node
    4. Send updated node_list to auto_scalar
    """

    instance = ec2_create()
    variables.pool_node_id_list.append(instance.id)

    thread = threading.Thread(target=run_cache_update_status, args=(instance.id,))
    thread.start()

    # time.sleep(10)
    # requests.post(config.AUTO_SCALAR_URL + "/api/scaler/cache_list", data={"node_list": variables.pool_node_id_list})
    return


def decrease_pool_size_manual():
    """
    1. Delete ec2 instance
    2. Update local node_list
    3. Send updated node_list to auto_scalar
    """

    instance = variables.pool_node_id_list[-1]
    ec2_destroy(instance.id)
    variables.pool_node_id_list.append(instance.id)
    # requests.post(config.AUTO_SCALAR_URL + "/api/scaler/cache_list", data={"node_list": variables.pool_node_id_list})
    return


def get_one_min_aggregate_data():
    miss_rate = 0
    hit_rate = 0
    cache_item_num = 0
    cache_total_size = 0
    request_served_num = 0
    for i in range(8):
        miss_rate += get_one_min_data(i, 'miss rate')
        hit_rate += get_one_min_data(i, 'hit rate')
        cache_item_num += get_one_min_data(i, 'number of keys added')
        cache_total_size += get_one_min_data(i, 'capacity used')
        request_served_num += get_one_min_data(i, 'request served')
    variables.miss_rate.append(miss_rate)
    variables.hit_rate.append(hit_rate)
    variables.cache_item_num.append(cache_item_num)
    variables.cache_total_size.append(cache_total_size)
    variables.request_served_num.append(request_served_num)
    return
