import requests
from flask import request, jsonify

import manager_app
from manager_app import variables, config
from manager_app.helper_functions.ec2_helper import ec2_get_instance_ip
from manager_app.helper_functions.manager_helper import generate_node_ip_list, increase_pool_size_manual, \
    decrease_pool_size_manual
from manager_app.helper_functions.responses import success_response, failed_response


def update_node_list():
    node_list = request.form.get('list')
    variables.pool_node_id_list = node_list
    return success_response(jsonify(node_list=node_list))


def get_pool_size():
    size = variables.pool_node_id_list.size()
    return success_response(jsonify(size=size))


# Rewrite
def get_pool_node_list():
    node_ip_list = []
    for instance_id in variables.pool_node_id_list:
        node_ip_list.append(ec2_get_instance_ip(instance_id))
    return success_response(jsonify(node_id_list=variables.pool_node_id_list,
                                    node_ip_list=node_ip_list))


def get_resize_pool_config():
    content = jsonify(
        resize_pool_option=variables.resize_pool_option,
        resize_pool_parameters=variables.resize_pool_parameters
    )
    return success_response(content)


# def get_30_min_data():
#     if manager_app.data_30_min.size >= 30:
#         manager_app.data_30_min.pop(0)
#     manager_app.data_30_min.append(get_stats_from_db())


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

    changed_node_ip = variables.pool_node_id_list[-1].public_ip_address
    response = requests.post(config.SERVER_URL + "/api/notify", data={"node_ip": [changed_node_ip],
                                                                      "mode": variables.resize_pool_option,
                                                                      "change": change})
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
    return success_response(content)


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
    1. Call instance 1 to clear cache
    """
    response = requests.delete(config.SERVER_URL + "/api/clear/cache")
    content = response["content"]
    return success_response(content)


def clear_all_data():
    """
    1. Call instance 1 to clear data
    """
    response = requests.delete(config.SERVER_URL + "/api/clear/data")
    content = response["content"]
    return success_response(content)
