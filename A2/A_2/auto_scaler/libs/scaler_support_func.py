from flask import json
import requests
import threading
import logging
import time

import sys
sys.path.append("../..") 
import auto_scaler.config as config
import auto_scaler.statistics as statistics
from auto_scaler import webapp

from auto_scaler.libs.ec2_support_func import ec2_create, ec2_destroy, ec2_get_instance_ip
from auto_scaler.libs.ssh_support_func import run_cache

def gen_failed_responce(code, message):
    json_response = {
        "success": "false",
        "error": {
            "code": code,
            "message": message
             }
    }
    response = webapp.response_class(
        response=json.dumps(json_response),
        status=400,
        mimetype='application/json'
    )
    return response

def gen_success_responce(content):
    json_response = {
            "success": "true",
            "content" : content
        }
    response = webapp.response_class(
        response=json.dumps(json_response),
        status=200,
        mimetype='application/json'
    )
    return response

def add_cache_node():
    instance = ec2_create()
    statistics.node_running[instance.id] = False
    
    thread = threading.Thread(target = run_cache_update_status, kwargs={'id' : instance.id}, daemon = True)
    thread.start()
    
    config.cache_pool_size += 1
    config.cache_pool_ids.append(instance.id)

def run_cache_update_status(id):
    time.sleep(1) # add small delay so the 'ec2.instances.filter' can find the newly created instance
    address = ec2_get_instance_ip(id)
    
    error_count = 0
    while True:
        try:
            time.sleep(10)
            run_cache(address)
            break
        except Exception as error:
            error_count += 1
            if error_count > 5:
                logging.error("run_cache_update_status - node with ip {} brought up failed! {}".format(address, error))
                return
            continue
    
    time.sleep(10)
    response = -1
    error_count = 0
    while True:
        try:
            time.sleep(1)
            response = get_memcache_statistics(address)
            if response == -1:
                logging.error("run_cache_update_status - node with ip {} access failed!".format(address))
            else:
                logging.info("run_cache_update_status - node with ip {} successfully brought up!".format(address))
                statistics.node_running[id] = True
                # once the cache node is up, refresh config and assign the node index
                response = requests.post("http://" + address + ":" + str(config.cache_port) + "/api/cache/config", \
                    data=[('capacity', config.capacity), ('replacement_policy', config.replacement_policy), ('cache_index', get_cache_index_from_id(id))])
            break
        except Exception as error:
            # cache is not responding
            error_count += 1
            if error_count < 10:
                continue
            else:
                logging.error("run_cache_update_status - node with ip {} access timeout! {}".format(address, error))
                return
    return

def get_cache_index_from_id(id):
    index = config.cache_pool_ids.index(id)
    return index

def remove_cache_node(id):
    ec2_destroy(id)
    del statistics.node_running[id]
    config.cache_pool_size -= 1
    config.cache_pool_ids.remove(id)

def initialization():
    add_cache_node()

def get_memcache_statistics(address):
    response = requests.get("http://" + address + ":" + str(config.cache_port) + "/api/cache/statistics")
    # response = requests.get("http://" + address + ":5001" + "" + "/api/cache/statistics")
    if response.status_code == 200:
        response = json.loads(response.content)
        if response["success"] == "true":
            return json.loads(response["content"])
        else:
            return -1
    else:
        return -1

def get_miss_rate(manully_triggered = False):
    if manully_triggered == False:
        total_get_request = 0
        total_hit = 0
        for i in range(len(config.cache_pool_ids)):
            if config.cache_pool_ids[i] in statistics.node_running and statistics.node_running[config.cache_pool_ids[i]] == True:
                addr = ec2_get_instance_ip(config.cache_pool_ids[i])
                status = get_memcache_statistics(addr)
                if i == 0:
                    # the first node exist from the beginning, so the get request it served 
                    # should be the number of total get request 
                    total_get_request = status['num_GET_request_served']
                total_hit += status['num_hit']
        if total_get_request == 0:
            return 'n/a'
        return (total_get_request - total_hit) / total_get_request
    else: # for testing only
        return statistics.test_miss_rate

def get_cache_pool_size():
    if config.auto_mode == True:
        return config.cache_pool_size
    else: # get the list of IDs of nodes from the manager-app
        # TODO: need to get it from the manager-app
        logging.error("get_cache_pool_size - config.auto_mode == True case not yet supported!")
        return config.cache_pool_size
