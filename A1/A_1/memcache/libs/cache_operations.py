from flask import render_template, request
import logging

import sys
sys.path.append("../..") 
import memcache.config as config
import memcache.statistics as statistics

from memcache.libs.cache_support_func import gen_failed_responce, invalidateKey, remove_element, \
    set_parameters, gen_success_responce, file_size
from memcache.libs.db_operations import db, get_config_from_db

def get_service():
    key = request.form.get('key')

    if key in config.memcache:
        value = config.memcache[key]
        # lest recently used key will be in index 0
        config.key_list.remove(key) # remove it from the list
        config.key_list.append(key) # add it to the end of the list
        statistics.num_hit = statistics.num_hit + 1
        
        response = gen_success_responce(value)
    else:
        response = gen_failed_responce(400, "Unknown key")
    
    statistics.num_request_served = statistics.num_request_served + 1
    statistics.num_GET_request_served = statistics.num_GET_request_served + 1

    print(config.key_list)
    return response

def put_service():
    # check if there is a key
    if request.form.get('key') == '':
        response = gen_failed_responce(400, "Missing key")
        return response
    # check if there is a value
    if request.form.get('value') == '':
        response = gen_failed_responce(400, "Missing value")
        return response
    
    # when there is a image been submitted proeprly
    key = request.form.get('key')
    value = request.form.get('value')
    # space check
    size = file_size(value)
    if size > config.capacity:
        response = gen_failed_responce(400, "File is bigger then the whole cache")
        return response
    # if the current key exist, remove it before adding so the used_size calculation is correct
    if key in config.key_list:
        invalidateKey(key)
    # if free space is not enough, do some replacement until cache is empty or having enough space
    if statistics.used_size + size > config.capacity: 
        while len(config.memcache) > 0 and statistics.used_size + size > config.capacity:
            remove_element()
    # once we have enough free space, save the file into the cache
    config.memcache[key] = value
    statistics.used_size = statistics.used_size + size
    statistics.num_item_in_cache = statistics.num_item_in_cache + 1
    statistics.num_request_served = statistics.num_request_served + 1
    # added to config.key_list to keep track of which one is been recently used
    if key in config.key_list:
        config.key_list.remove(key) # remove it from the list
        config.key_list.append(key) # add it to the end of the list
    else:
        config.key_list.append(key) # add it to the end of the list
    
    logging.debug('put - key: ' + key + ' with len(value) of ' + str(size) + ' added to the cache')
    logging.info('put - cache used = ' + str(statistics.used_size))
        
    # make the correct response
    response = gen_success_responce("")
    print(config.key_list)
    return response

# remove key, key will be passed from the from
def remove_key_service():
    key = request.form.get('key')
    if key in config.memcache:
        invalidateKey(key)
    # make the correct response
    response = gen_success_responce("")
    return response

# to read mem-cache related details from the database and reconfigure it based 
# on the values set by the user
def refreshConfiguration_service():
    data = get_config_from_db()
    new_capacity = data['capacity']
    new_replacement_policy = data['policy']
    
    (code, msg) = set_parameters(new_capacity, new_replacement_policy)
    logging.info('refreshConfiguration - capacity = ' + str(config.capacity) + ', replacement policy = ' + config.replace)
    if code == 200:
        # make the correct response
        response = gen_success_responce("")
        return response
    else:
        response = gen_failed_responce(code, msg)
        return response
    
def clear_service():
    config.memcache = {}
    config.key_list = []
    statistics.used_size = 0
    logging.debug('CLEAR - cache cleared')
    
    # make the correct response
    response = gen_success_responce("")
    
    return response

# for testing only
def show_info_service():
    query = ("SELECT cache_nums, used_size, total_request_served, total_GET_request_served, total_hit "
             "FROM status ORDER BY id DESC LIMIT 120;")
    data = db.SQL_command(query)
    
    (num_key_added_end, used_size_end, request_served_end, GET_request_served_end, num_hit_end) = data[0]
    (num_key_added_start, used_size_start, request_served_start, GET_request_served_start, num_hit_start) = data[-1]
    num_key_added_10min = num_key_added_end - num_key_added_start
    used_size_10min = used_size_end - used_size_start
    request_served_10min = request_served_end - request_served_start
    GET_request_served_10min = GET_request_served_end - GET_request_served_start
    num_hit_10min = num_hit_end - num_hit_start
    if GET_request_served_10min != 0:
        hit_rate_10min = num_hit_10min / GET_request_served_10min
        miss_rate_10min = 1 - hit_rate_10min
    else:
        hit_rate_10min = "n/a"
        miss_rate_10min = "n/a"

    if statistics.num_GET_request_served != 0:
        hit_rate = statistics.num_hit / statistics.num_GET_request_served
        miss_rate = 1 - hit_rate
    else:
        hit_rate = "n/a"
        miss_rate = "n/a"
        
    return render_template("info.html", capacity = config.capacity, replacement_policy = config.replace, \
                           total_num_item_in_cache = statistics.num_item_in_cache, total_used_size = statistics.used_size, \
                           total_request_served = statistics.num_request_served, total_hit = statistics.num_hit, \
                           total_miss_rate = miss_rate, total_hit_rate = hit_rate, \
                           num_key_added_10min = num_key_added_10min, used_size_10min = used_size_10min, \
                           request_served_10min = request_served_10min, miss_rate_10min = miss_rate_10min, \
                           hit_rate_10min = hit_rate_10min)