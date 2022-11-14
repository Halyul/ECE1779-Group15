import requests

from manager_app import variables, config
from manager_app.helper_functions.ec2_helper import ec2_create, ec2_destroy


def generate_node_ip_list():
    ip_list = []
    for instance in variables.pool_node_id_list:
        ip_list.append(instance.public_ip_address)
    return ip_list


def increase_pool_size_manual():
    """
    1. Create ec2 instance
    2. Update local node_list
    3. Send updated node_list to auto_scalar
    """

    instance = ec2_create()
    variables.pool_node_id_list.append(instance.id)
    # Rewrite: confirm the URL to update node list, confirm body
    requests.post(config.AUTO_SCALAR_URL + "/api/scaler/cache_list", data={"node_list": variables.pool_node_id_list})
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
    # Rewrite: confirm the URL to update node list, confirm body
    requests.post(config.AUTO_SCALAR_URL + "/api/scaler/cache_list", data={"node_list": variables.pool_node_id_list})
    return


def task_queue():
    return
