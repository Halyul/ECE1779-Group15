from flask import json
import requests
import threading 

import sys
sys.path.append("../..") 
import auto_scaler.config as config
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
    #TODO: make the run_cache work
    # run_cache(instance.id)
    config.cache_pool_size += 1
    config.cache_pool_ids.append(instance.id)

def run_cache_update_status(id):
    run_cache(id)
    
    return 0

def remove_cache_node(id):
    ec2_destroy(id)
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

def get_miss_rate():
    # FIXME: need to put these back once memcache works fine
    # total_get_request = 0
    # total_hit = 0
    # for i in range(len(config.cache_pool_ids)):
    #     addr = ec2_get_instance_ip(config.cache_pool_ids[i])
    #     status = get_memcache_statistics(addr)
    #     if i == 0:
    #         # the first node exist from the beginning, so the get request it served 
    #         # should be the number of total get request 
    #         total_get_request = status['num_GET_request_served']
    #     total_hit += status['num_hit']
    # if total_get_request == 0:
    #     return ""
    # return (total_get_request - total_hit) / total_get_request
    return 0

def get_cache_pool_size():
    if config.auto_mode == True:
        return config.cache_pool_size
    else: # get the list of IDs of nodes from the manager-app
        # TODO: need to get it from the manager-app
        return config.cache_pool_size
