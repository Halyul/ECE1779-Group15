import requests

from manager_app import variables, config
from manager_app.helper_functions.ec2_helper import ec2_create, ec2_destroy


def generate_node_ip_list():
    ip_list = []
    for instance in variables.memcache_pool_node_list:
        ip_list.append(instance.public_ip_address)
    return ip_list


def increase_pool_size_manual():
    """
    1. Create ec2 instance
    2. Update local node_list
    3. Send updated node_list to auto_scalar
    """

    instance = ec2_create()
    variables.memcache_pool_node_list.append(instance)
    # Rewrite: confirm the URL to update node list, confirm body
    requests.post(config.AUTO_SCALAR_URL + "/api/node_list", data={"node_list": variables.memcache_pool_node_list})
    return


def decrease_pool_size_manual():
    """
    1. Delete ec2 instance
    2. Update local node_list
    3. Send updated node_list to auto_scalar
    """

    instance = variables.memcache_pool_node_list[-1]
    ec2_destroy(instance.id)
    variables.memcache_pool_node_list.append(instance)
    # Rewrite: confirm the URL to update node list, confirm body
    requests.post(config.AUTO_SCALAR_URL + "/api/node_list", data={"node_list": variables.memcache_pool_node_list})
    return
