import requests
from flask import request, jsonify

import manager_app
from manager_app import variables, config
from manager_app.helper_functions.manager_helper import generate_node_ip_list, increase_pool_size_manual, \
    decrease_pool_size_manual
from manager_app.helper_functions.responses import success_response, failed_response
from manager_app.helper_functions.s3_helper import s3_list, s3_clear


def get_pool_size():
    # Rewrite: get size from ec2 filtered by subnet
    # Node list only got updated when switching from auto -> manual
    size = variables.memcache_pool_node_list.size()
    return jsonify(size=size)


def get_pool_node_list():
    return jsonify(pool_node_list=variables.memcache_pool_node_list)


def get_resize_pool_config():
    content = jsonify(
        resize_pool_option=variables.resize_pool_option,
        resize_pool_parameters=variables.resize_pool_parameters
    )
    return content


def get_30_min_data():
    if manager_app.data_30_min.size >= 30:
        manager_app.data_30_min.pop(0)
    manager_app.data_30_min.append(get_stats_from_db())


def task_queue():
    return


def notify_pool_size_change():
    """
    1. Store change request (increase/decrease) to local
    2. Update local resize_pool_option to manual
    3. Check if pool size minimum/maximum. No following actions if it is.
    4. If increasing, increase pool size, notify instance 1
    5. If decreasing, notify instance 1
    """
    change = request.form.get('change')
    variables.manual_operation = change
    manager_app.resize_pool_option = 'manual'
    manager_app.resize_pool_parameters = {}
    pool_size = get_pool_size()

    if change == 'increase':
        if pool_size == 8:
            return failed_response(400, "The size of memcache pool has been reached to maximum")
        else:
            increase_pool_size_manual()
    elif change == 'decrease':
        if pool_size == 1:
            return failed_response(400, "The size of memcache pool has been reached to minimum")
    else:
        return failed_response(400, "Parameter change can only be increase or decrease")
    # Rewrite, confirm URL, confirm data body: one instance/instance_list, ip or instance
    changed_node_ip = variables.memcache_pool_node_list[-1].public_ip_address
    response = requests.post(config.SERVER_URL + "/api/pool_size_change", data={"node_ip": changed_node_ip})
    content = response["content"]
    return success_response(content)


def change_pool_size_manual():
    """
    1. When key-image move is done, check stored change variable
    2. If request was increase, do nothing, since pool size has been increased before
    3. If request was decrease, decrease pool size
    """
    change = variables.manual_operation
    if change == 'increase':
        return success_response("Memcache pool size increases")
    else:
        decrease_pool_size_manual()
        return success_response("Memcache pool size decreases")


def set_auto_scaler_parameters():
    """
    1. Update local resize_pool_option to automatic, and store parameters
    2. Pass parameters to auto_scalar
    """
    max_miss_rate_threshold = request.form.get('max_miss_rate_threshold')
    min_miss_rate_threshold = request.form.get('min_miss_rate_threshold')
    ratio_expand_pool = request.form.get('ratio_expand_pool')
    ratio_shrink_pool = request.form.get('ratio_shrink_pool')

    parameters = {'max_miss_rate_threshold': max_miss_rate_threshold,
                  'min_miss_rate_threshold': min_miss_rate_threshold,
                  'ratio_expand_pool': ratio_expand_pool,
                  'ratio_shrink_pool': ratio_shrink_pool,
                  'auto_mode': 'True'}

    manager_app.resize_pool_option = 'automatic'
    manager_app.resize_pool_parameters = parameters

    response = requests.post(config.AUTO_SCALAR_URL + "/api/scaler/config",
                             data=parameters)
    content = response["content"]
    return success_response(content)


def get_cache_configurations():
    content = jsonify(
        capacity=variables.memcache_capacity,
        replacement_policy=variables.memcache_replacement_policy
    )
    return content


def set_cache_configurations():
    """
    1. Get running node ip
    2. Store cache configs to local
    3. For each ip, call instance 2 set cache config
    """
    capacity = request.form.get('capacity')
    replacement_policy = request.form.get('replacement_policy')
    variables.memcache_capacity = capacity
    variables.memcache_replacement_policy = replacement_policy

    content = []
    ip_list = generate_node_ip_list()
    for ip in ip_list:
        node_url = ip + ":" + config.cache_port
        response = requests.post(node_url + "/api/cache/config",
                                 data={'capacity': capacity,
                                       'replacement_policy': replacement_policy})
        content.append(response["content"])
    return success_response(content)


def clear_all_cache():
    """
    1. Get running node ip
    2. For each ip, call instance 2 clear all cache
    """
    content = []
    ip_list = generate_node_ip_list()
    for ip in ip_list:
        node_url = ip + ":" + config.cache_port
        response = requests.delete(node_url + "/api/cache")
        content.append(response["content"])
    return success_response(content)


def clear_all_data():
    """
    1. Clear all cache
    2. Clear s3 buckets
    3. Clear RDS
    """
    clear_all_cache()

    buckets = s3_list()
    s3_clear(buckets[0])

    # RDS
