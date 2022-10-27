from flask import render_template, request, redirect, url_for
import logging
import time
import numpy as np

import sys
sys.path.append("../..") 
import auto_scaler.config as config
import json

from auto_scaler.libs.scaler_support_func import gen_failed_responce, gen_success_responce, get_miss_rate, \
    get_cache_pool_size, remove_cache_node, add_cache_node
from auto_scaler.libs.ec2_support_func import ec2_list, ec2_get_instance_ip

def responce_main():
    data = {}
    data['miss_rate'] = get_miss_rate()
    data['auto_mode'] = config.auto_mode
    data['cache_pool_size'] = config.cache_pool_size
    data['max_miss_rate_threshold'] = config.max_miss_rate_threshold
    data['min_miss_rate_threshold'] = config.min_miss_rate_threshold
    data['expand_ratio'] = config.expand_ratio
    data['shrink_ratio'] = config.shrink_ratio
    
    instances = []
    for instance_id in config.cache_pool_ids:
        instance = {}
        instance['id'] = instance_id
        instance['address'] = ec2_get_instance_ip(instance_id)
        instances.append(instance)
    return render_template("info.html", data = data, instances = instances)

def responce_refresh_config():
    try:
        new_config = json.loads(request.form.get('config'))
        
        config.max_miss_rate_threshold = new_config['max_miss_rate_threshold']
        config.min_miss_rate_threshold = new_config['min_miss_rate_threshold']
        config.expand_ratio = new_config['expand_ratio']
        config.shrink_ratio = new_config['shrink_ratio']
        config.auto_mode = new_config['auto_mode']
        
        return gen_success_responce("")
    except Exception as error:
        logging.error('responce_refresh_config - ' + error)
        return gen_failed_responce(400, error)
    
def check_miss_rate_every_min():
    miss_rate = get_miss_rate()
    
    if config.auto_mode == True:
        if miss_rate < config.min_miss_rate_threshold:
            expected_pool_size = get_cache_pool_size() / config.shrink_ratio
        elif miss_rate > config.max_miss_rate_threshold:
            expected_pool_size = get_cache_pool_size() * config.expand_ratio
        
        expected_pool_size = np.clip(round(expected_pool_size), 1, 8)
        while expected_pool_size != get_cache_pool_size():
            if expected_pool_size > get_cache_pool_size():
                add_cache_node()
            else:
                remove_cache_node(config.cache_pool_ids[-1])
    
    time.sleep(60)
    return miss_rate

# for testing
def responce_terminate_all():
    for instance_id in config.cache_pool_ids:
        remove_cache_node(instance_id)
    return redirect(url_for('main'))

# for testing
def responce_list_cache():
    instances = ec2_list("all")
    return render_template("list.html", instances = instances)