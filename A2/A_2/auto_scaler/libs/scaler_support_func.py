from flask import json, request
import requests
import threading
import logging
import time
from datetime import datetime, timedelta

import sys
sys.path.append("../..") 
import auto_scaler.config as config
import auto_scaler.statistics as statistics
from auto_scaler import webapp

from auto_scaler.libs.ec2_support_func import ec2_create, ec2_destroy, ec2_get_instance_ip, ec2_get_instance_ip
from auto_scaler.libs.ssh_support_func import run_cache
from auto_scaler.libs.cloudwatch_func import get_num_GET_request_served, get_num_hit

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

    error_count = 0
    while True:
        try:
            time.sleep(10)
            address = ec2_get_instance_ip(id)
            run_cache(address)
            break
        except Exception as error:
            error_count += 1
            if error_count > 5:
                logging.error("run_cache_update_status - node with ip {} brought up failed! {}".format(address, error))
                return
            continue
    
    time.sleep(10)
    check_if_node_is_up(id, address)
    return

def check_if_node_is_up(id, address):
    response = -1
    error_count = 0

    # if the address from input is incorrect, re-get the address (may due to node is not fully running while getting the address)
    # if it is still 'None', return -1
    if address is None or len(address) > 15:
        address = ec2_get_instance_ip(id)
        if address is None or len(address) > 15:
            logging.error("check_if_node_is_up - ip incorrect! id = {}, ip = {}".format(id, address))
            return -1

    while True:
        try:
            time.sleep(1)
            response = get_memcache_statistics(address)
            if response == -1:
                logging.error("check_if_node_is_up - node with ip {} access failed!".format(address))
                return -1
            else:
                logging.info("check_if_node_is_up - node with ip {} successfully brought up!".format(address))
                if statistics.node_running[id] == False:
                    statistics.node_running[id] = True
                # once the cache node is up, refresh config and assign the node index
                response = requests.post("http://" + address + ":" + str(config.cache_port) + "/api/cache/config", \
                    data=[('capacity', config.capacity), ('replacement_policy', config.replacement_policy), ('cache_index', get_cache_index_from_id(id))])
            break
        except Exception as error:
            # cache is not responding
            error_count += 1
            if error_count < 20:
                continue
            else:
                logging.error("check_if_node_is_up - node with ip {} access timeout! {}".format(address, error))
                return -1
    return 0

def get_cache_index_from_id(id):
    index = config.cache_pool_ids.index(id)
    return index

def remove_cache_node(id):
    ec2_destroy(id)
    del statistics.node_running[id]
    config.cache_pool_size -= 1
    config.cache_pool_ids.remove(id)

def clear_cache_node():
    for instance_id in config.cache_pool_ids:
        ec2_destroy(instance_id)
        del statistics.node_running[instance_id]
    config.cache_pool_size = 0
    config.cache_pool_ids = []

def initialization():
    add_cache_node()

# will be used only for checking if the node is up
# statistics will be fetched from CloudWatch as requirement stated
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
        # read total_get_request and total_hit from CloudWatch
        for i in range(len(config.cache_pool_ids)):
            if config.cache_pool_ids[i] in statistics.node_running and statistics.node_running[config.cache_pool_ids[i]] == True:
                # logging.info("reading statistics from cloudwatch, i = {}".format(i))
                cloudwatch_num_hit = get_num_hit(i)
                if cloudwatch_num_hit != []:
                    total_hit += cloudwatch_num_hit[0]
                cloudwatch_num_GET_request_served = get_num_GET_request_served(i)
                if cloudwatch_num_GET_request_served != []:
                    total_get_request += cloudwatch_num_GET_request_served[0]
                # logging.info("statistics: total_hit = {}, total_get_request = {}".format(total_hit, total_get_request))
        # start calculating the miss rate
        if total_get_request == 0:
            return 'n/a'
        logging.info("get_miss_rate - total_get_request = {}, total_hit = {}".format(total_get_request, total_hit))
        return (total_get_request - total_hit) / total_get_request
    else: # for testing only
        return statistics.test_miss_rate

def get_cache_pool_size():
    if config.auto_mode == True:
        return config.cache_pool_size
    else: 
        # TODO: get the node list from manager, or manager need to send the list every time list updated
        refresh_node_list()
        return config.cache_pool_size

def clear_all_cache_stats():
    for node_id in statistics.node_running:
        if statistics.node_running[node_id] == True:
            address = ec2_get_instance_ip(node_id)
            response = requests.delete("http://" + address + ":" + str(config.cache_port) + "/api/cache/statistics")
        # else:
        #     # if this node is in the list but not running, check again if it is running
        #     addr = ec2_get_instance_ip(node_id)
        #     thread = threading.Thread(target = check_if_node_is_up, args=(node_id, addr), daemon = True)
        #     thread.start()
    return 

def notify_while_bring_up_node(notify_info, changed_id):
    start_time = datetime.now()
    all_running = False
    while all_running == False:
        time.sleep(1)
        if datetime.now() > (start_time + timedelta(minutes=2)):
            logging.error("notify_while_bring_up_node - node {} not responding!".format(id))
            return
        # wait until all nodes are running or a timeout after 2mins
        all_running = True
        for id in changed_id:
            if statistics.node_running[id] == False:
                all_running = False
                break
            else:
                ip = ec2_get_instance_ip(id)
                if ip not in notify_info['ip']:
                    notify_info['ip'].append(ip)
    logging.info("notify_while_bring_up_node - all new nodes are up, sending request to notify A1")
    logging.info("notify_while_bring_up_node - notify_info = {}".format(json.dumps(notify_info)))
    # TODO: enable this line and makes sure format matches with A1
    # response = requests.post('http://127.0.0.1:' + str(config.server_port) + '/api/notify', data=[('ip', notify_info['ip']), ('mode', 'automatic'), ('change', 'increase')])
    return

def refresh_node_list():
    if config.auto_mode == True:
        return
    else:
        # get the node_list from manager and process the listif in manaul mode
        node_list = []
        response = requests.get("http://127.0.0.1:" + str(config.manager_port) + "/api/manager/pool_node_list")
        node_dict = json.loads(response.content)['pool_node_list']
        for node_id in node_dict:
            node_list.append(node_id)

        set_node_list_from_node_list(node_list)
        return

def set_node_list_from_node_list(node_list):
    if config.auto_mode == False:
        config.cache_pool_ids = node_list
        config.cache_pool_size = len(config.cache_pool_ids)
        # refresh the statistics.node_running
        statistics.node_running = {}
        unrunning_node = []
        for node_id in node_list:
            statistics.node_running[node_id] = False
            addr = ec2_get_instance_ip(node_id)
            is_running =  check_if_node_is_up(node_id, addr)
            if is_running == -1:
                unrunning_node.append(node_id)
        if len(unrunning_node) == 0:
            return gen_success_responce("")
        else:
            logging.error("Some nodes are not running! {}".format(json.dumps(unrunning_node)))
            return gen_failed_responce(400, "Some nodes are not running! {}".format(json.dumps(unrunning_node)))
    else:
        logging.error("Should not set node_list from outside while auto mode!")
        return gen_failed_responce(400, "Should not set node_list from outside while auto mode!")