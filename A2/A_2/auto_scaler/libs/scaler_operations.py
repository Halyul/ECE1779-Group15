from flask import render_template, request, redirect, url_for
import logging
import time
import numpy as np

import sys
sys.path.append("../..") 
import auto_scaler.config as config

from auto_scaler.libs.scaler_support_func import gen_failed_responce, gen_success_responce, get_miss_rate, \
    get_cache_pool_size, remove_cache_node, add_cache_node, clear_cache_node, clear_all_cache_stats, update_pool_size_use_ec2
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
        # max_miss_rate_threshold and min_miss_rate_threshold should between in range [0,1]
        if float(request.form.get('max_miss_rate_threshold')) < 0 or float(request.form.get('max_miss_rate_threshold')) > 1:
            gen_failed_responce(400, "max_miss_rate_threshold = {} which is not valid".format(float(request.form.get('max_miss_rate_threshold'))))
        if float(request.form.get('min_miss_rate_threshold')) < 0 or float(request.form.get('min_miss_rate_threshold')) > 1:
            gen_failed_responce(400, "min_miss_rate_threshold = {} which is not valid".format(float(request.form.get('min_miss_rate_threshold'))))
        config.max_miss_rate_threshold = float(request.form.get('max_miss_rate_threshold'))
        config.min_miss_rate_threshold = float(request.form.get('min_miss_rate_threshold'))
        # expand_ratio should be in range (1, inf)
        if float(request.form.get('expand_ratio')) <= 1:
            gen_failed_responce(400, "expand_ratio = {} which is not valid".format(float(request.form.get('expand_ratio'))))
        config.expand_ratio = float(request.form.get('expand_ratio'))
        # shrink_ratio should be in range (0, 1)
        if float(request.form.get('shrink_ratio')) >= 1 or float(request.form.get('shrink_ratio')) <= 0:
            gen_failed_responce(400, "shrink_ratio = {} which is not valid".format(float(request.form.get('shrink_ratio'))))
        config.shrink_ratio = float(request.form.get('shrink_ratio'))
        config.auto_mode = request.form.get('auto_mode') == 'True' or request.form.get('auto_mode') == 'true'
        
        return gen_success_responce("")
    except Exception as error:
        logging.error('responce_refresh_config - ' + error)
        return gen_failed_responce(400, error)
    
def check_miss_rate_every_min(manully_triggered = False):
    try:
        while True:
            miss_rate = get_miss_rate(manully_triggered = manully_triggered)
            
            if config.auto_mode == True and miss_rate != 'n/a':
                expected_pool_size = get_cache_pool_size()
                if miss_rate < config.min_miss_rate_threshold:
                    expected_pool_size = get_cache_pool_size() / config.shrink_ratio
                elif miss_rate > config.max_miss_rate_threshold:
                    expected_pool_size = get_cache_pool_size() * config.expand_ratio
                
                expected_pool_size = np.clip(round(expected_pool_size), 1, 8)
                logging.info("check_miss_rate_every_min - adjusting pool size: miss_rate = {}, expected_pool_size = {}, curr_pool_size = {}".format(miss_rate, expected_pool_size, get_cache_pool_size()))
                if expected_pool_size != get_cache_pool_size():
                    clear_all_cache_stats() # clear cache num_GET_request_served and num_hit if pool size needs adjustment
                while expected_pool_size != get_cache_pool_size():
                    if expected_pool_size > get_cache_pool_size():
                        add_cache_node()
                    else:
                        remove_cache_node(config.cache_pool_ids[-1])
            elif config.auto_mode == False:
                # TODO: need to get it from manager
                pass

            # if this update of num cache nodes is manully triggered, will return after one round of pool size update
            if manully_triggered == True:
                return miss_rate
            time.sleep(60)
    except Exception as error:
        logging.error("background update terminated! {}".format(error))
    return

# for testing
def responce_terminate_all():
    clear_cache_node()
    return redirect(url_for('main'))

# for testing
def responce_list_cache():
    instances = ec2_list("all")
    return render_template("list.html", instances = instances)