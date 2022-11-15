import logging
import time

import requests

from auto_scaler.libs.ssh_support_func import run_cache
from manager_app import config, variables
from manager_app.helper_functions.ec2_helper import ec2_get_instance_ip


def run_cache_update_status(node_id):
    """
    1. Run instance2 on new node
    2. Set cache config for new node
    3. Notifying instance 1
    """

    error_count = 0
    while True:
        try:
            time.sleep(10)
            address = ec2_get_instance_ip(node_id)
            run_cache(address)
            break
        except Exception as error:
            error_count += 1
            if error_count > 5:
                logging.error("run_cache_update_status - node with ip {} brought up failed! {}".format(address, error))
                return
            continue

    error_count = 0
    while True:
        try:
            time.sleep(10)
            address = ec2_get_instance_ip(node_id)
            node_url = "http://" + address + ":" + str(config.cache_port)
            response = requests.post(node_url + "/api/cache/config",
                                     data={'capacity': variables.memcache_capacity,
                                           'replacement_policy': variables.memcache_replacement_policy})
            logging.info("Instance 2 is running, setting cache config")
            logging.info(response.json()["success"])
            break
        except Exception as error:
            error_count += 1
            if error_count > 5:
                logging.error("Set cache config on {} failed due to {}".format(address, error))
                return
            continue

    error_count = 0
    if len(variables.pool_node_id_list) > 1:
        while True:
            try:
                address = ec2_get_instance_ip(node_id)
                requests.post(config.SERVER_URL + "/api/notify", json={"node_ip": [address],
                                                                       "mode": variables.resize_pool_option,
                                                                       "change": variables.manual_operation})
                logging.info("Notifying instance 1")
                break
            except Exception as error:
                error_count += 1
                if error_count > 5:
                    logging.error("Notifying instance 1 changing {} failed due to {}".format(address, error))
                    return
                continue
    return
