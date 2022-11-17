from flask import render_template, request, redirect, url_for
import logging
import time
import requests
import threading
import numpy as np
import json

import sys
sys.path.append("../..") 
import auto_scaler.config as config
import auto_scaler.statistics as statistics

from auto_scaler.libs.scaler_support_func import gen_failed_responce, gen_success_responce, get_miss_rate, \
    get_cache_pool_size, remove_cache_node, add_cache_node, clear_cache_node, clear_all_cache_stats, \
    notify_while_resize_pool, check_if_node_is_up, refresh_node_list, set_node_list_from_node_list
from auto_scaler.libs.ec2_support_func import ec2_list, ec2_get_instance_ip

def responce_main():
    if config.auto_mode == False:
        # get node_list from manager
        refresh_node_list() # will take some time
        pass

    data = {}
    data['miss_rate'] = get_miss_rate()
    data['auto_mode'] = config.auto_mode
    data['cache_pool_size'] = config.cache_pool_size
    data['max_miss_rate_threshold'] = config.max_miss_rate_threshold
    data['min_miss_rate_threshold'] = config.min_miss_rate_threshold
    data['expand_ratio'] = config.expand_ratio
    data['shrink_ratio'] = config.shrink_ratio
    data['capacity'] = config.capacity
    data['replacement_policy'] = config.replacement_policy
    
    instances = []
    for instance_id in config.cache_pool_ids:
        instance = {}
        instance['id'] = instance_id
        instance['address'] = ec2_get_instance_ip(instance_id)
        instance['is_running'] = statistics.node_running[instance_id]
        instances.append(instance)
    return render_template("info.html", data = data, instances = instances)

def responce_refresh_config():
    try:
        # max_miss_rate_threshold and min_miss_rate_threshold should between in range [0,1]
        if float(request.form.get('max_miss_rate_threshold')) < 0 or float(request.form.get('max_miss_rate_threshold')) > 1:
            return gen_failed_responce(400, "max_miss_rate_threshold = {} which is not valid".format(float(request.form.get('max_miss_rate_threshold'))))
        if float(request.form.get('min_miss_rate_threshold')) < 0 or float(request.form.get('min_miss_rate_threshold')) > 1:
            return gen_failed_responce(400, "min_miss_rate_threshold = {} which is not valid".format(float(request.form.get('min_miss_rate_threshold'))))
        config.max_miss_rate_threshold = float(request.form.get('max_miss_rate_threshold'))
        config.min_miss_rate_threshold = float(request.form.get('min_miss_rate_threshold'))
        # expand_ratio should be in range (1, inf)
        if float(request.form.get('ratio_expand_pool')) <= 1:
            return gen_failed_responce(400, "ratio_expand_pool = {} which is not valid".format(float(request.form.get('ratio_expand_pool'))))
        config.expand_ratio = float(request.form.get('ratio_expand_pool'))
        # shrink_ratio should be in range (0, 1) ratio_shrink_pool
        if float(request.form.get('ratio_shrink_pool')) >= 1 or float(request.form.get('ratio_shrink_pool')) <= 0:
            return gen_failed_responce(400, "ratio_shrink_pool = {} which is not valid".format(float(request.form.get('ratio_shrink_pool'))))
        config.shrink_ratio = float(request.form.get('ratio_shrink_pool'))
        
        if config.auto_mode == False and (request.form.get('auto_mode') == 'True' or request.form.get('auto_mode') == 'true'):
            # if auto_mode changed from False to True, force a poolsize update
            config.auto_mode = request.form.get('auto_mode') == 'True' or request.form.get('auto_mode') == 'true'
            check_miss_rate_every_min(manully_triggered = True)
        else:
            config.auto_mode = request.form.get('auto_mode') == 'True' or request.form.get('auto_mode') == 'true'

        return gen_success_responce("")
    except Exception as error:
        logging.error('responce_refresh_config - {}'.format(error))
        return gen_failed_responce(400, error)
    
def responce_refresh_cache_config():
    try:
        if int(request.form.get('capacity')) < 0:
            return gen_failed_responce(400, "capacity = {} which is not valid".format(int(request.form.get('capacity'))))
        if request.form.get('replacement_policy') not in ['rr', 'lru']:
            return gen_failed_responce(400, "replacement_policy = {} which is not valid".format(request.form.get('replacement_policy')))
        config.capacity = int(request.form.get('capacity'))
        config.replacement_policy = request.form.get('replacement_policy')

        # refresh nodes running status
        for node_id in statistics.node_running:
            if statistics.node_running[node_id] == False:
                node_addr = ec2_get_instance_ip(node_id)
                check_if_node_is_up(node_id, node_addr)
        # refresh config for all nodes that are running if auto_mode is on
        if config.auto_mode == True:
            for node_id in statistics.node_running:
                if statistics.node_running[node_id] == True:
                    node_addr = ec2_get_instance_ip(node_id)
                    response = requests.post("http://" + node_addr + ":" + str(config.cache_port) + "/api/cache/config", \
                        data=[('capacity', config.capacity), ('replacement_policy', config.replacement_policy)])

        return gen_success_responce("")
    except Exception as error:
        logging.error('responce_refresh_cache_config - ' + error)
        return gen_failed_responce(400, error)

def check_miss_rate_every_min(manully_triggered = False):
    try:
        while True:
            # refresh nodes running status
            for node_id in statistics.node_running:
                if statistics.node_running[node_id] == False:
                    node_addr = ec2_get_instance_ip(node_id)
                    thread = threading.Thread(target = check_if_node_is_up, args=(node_id, node_addr,), daemon = True)
                    thread.start()

            notify_info = {'action' : '', 'ip' : []}
            changed_id = []
            miss_rate = get_miss_rate(manully_triggered = manully_triggered)
            # if miss_rate is 'n/a', means no one is using any of the cache, so to decrease the pool size
            if miss_rate == 'n/a':
                miss_rate = 0
            
            if config.auto_mode == True and miss_rate != 'n/a':
                expected_pool_size = get_cache_pool_size()
                if miss_rate < config.min_miss_rate_threshold:
                    expected_pool_size = get_cache_pool_size() * config.shrink_ratio
                elif miss_rate > config.max_miss_rate_threshold:
                    expected_pool_size = get_cache_pool_size() * config.expand_ratio
                
                expected_pool_size = np.clip(round(expected_pool_size), 1, 8)
                logging.info("check_miss_rate_every_min - adjusting pool size: miss_rate = {}, expected_pool_size = {}, curr_pool_size = {}".format(miss_rate, expected_pool_size, get_cache_pool_size()))
                original_pool_size = get_cache_pool_size()
                # temtitive_pool_size is used since delete node will need to send request to other flask instance
                temtitive_pool_size = get_cache_pool_size()
                while expected_pool_size != temtitive_pool_size:
                    if expected_pool_size > get_cache_pool_size():
                        add_cache_node()
                        temtitive_pool_size += 1
                        notify_info['action'] = 'add'
                        changed_id.append(config.cache_pool_ids[-1])
                    else:
                        temtitive_pool_size -= 1
                        notify_info['action'] = 'delete'
                        # notify_info['ip'].append(ec2_get_instance_ip(config.cache_pool_ids[-1 - len(notify_info['ip'])]))
                        changed_id.append(config.cache_pool_ids[-1 - len(changed_id)])
                if expected_pool_size != original_pool_size:
                    # clear cache num_GET_request_served and num_hit if pool size needs adjustment
                    clear_all_cache_stats()
                    # wait for nodes bring up, notify_while_resize_pool will notify A1 these changed nodes
                    thread = threading.Thread(target = notify_while_resize_pool, args=(notify_info, changed_id,), daemon = True)
                    thread.start()
                        
            elif config.auto_mode == False:
                # get node_list from manager
                refresh_node_list() # will take some time
                pass

            # if this update of num cache nodes is manully triggered, will return after one round of pool size update
            if manully_triggered == True:
                return miss_rate
            time.sleep(60)
    except Exception as error:
        logging.error("background update terminated! {}".format(error))
    return

def responce_do_node_delete():
    if len(config.cache_pool_ids) > 1:
        try:
            # for testing only
            cache_ip = request.form.get('cache_ip')
        except:
            cache_ip = request.environ['REMOTE_ADDR']
        cache_id = ''
        for id in config.cache_pool_ids:
            if cache_ip == ec2_get_instance_ip(id):
                cache_id = id
                break
        
        if cache_id == '':
            logging.error('responce_do_node_delete - No node with ip {}'.format(cache_ip))
            return gen_failed_responce(400, 'responce_do_node_delete - No node with ip {}'.format(cache_ip))
        elif cache_id == config.cache_pool_ids[0]:
            logging.error('responce_do_node_delete - Node with ip {} is the first node, and should never be deleted'.format(cache_ip))
            return gen_failed_responce(400, 'responce_do_node_delete - Node with ip {} is the first node, and should never be deleted'.format(cache_ip))
        else:
            remove_cache_node(cache_id)
            return gen_success_responce("")
    else:
        logging.error("responce_do_node_delete - pool size = {} so no nodes can be deleted".format(config.cache_pool_size))
        return gen_failed_responce(400, "responce_do_node_delete - pool size = {} so no nodes can be deleted".format(config.cache_pool_size))

def responce_get_node_list():
    return json.dumps(config.cache_pool_ids)

def responce_set_node_list(node_list = []):
    node_list = json.loads(request.form.get('cache_pool_ids'))
    response = set_node_list_from_node_list(node_list)
    return response

# for testing
def responce_terminate_all():
    clear_cache_node()
    return redirect(url_for('main'))

# for testing
def responce_list_cache():
    instances = ec2_list("all")
    return render_template("list.html", instances = instances)