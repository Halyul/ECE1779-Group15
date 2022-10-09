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
        statistics.num_hit_5s = statistics.num_hit_5s + 1
        
        response = gen_success_responce(value)
    else:
        response = gen_failed_responce(400, "Unknown key")
    
    statistics.num_request_served_5s = statistics.num_request_served_5s + 1
    print(config.key_list)
    return response

def put_service():
    logging.info("test")
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
    # added to config.key_list to keep track of which one is been recently used
    if key in config.key_list:
        config.key_list.remove(key) # remove it from the list
        config.key_list.append(key) # add it to the end of the list
    else:
        config.key_list.append(key) # add it to the end of the list
    statistics.item_added_5s = statistics.item_added_5s + 1
    statistics.capacity_used_5s = statistics.capacity_used_5s + size
    
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
    statistics.capacity_used_5s = statistics.capacity_used_5s - statistics.used_size
    statistics.used_size = 0
    logging.debug('CLEAR - cache cleared')
    
    # make the correct response
    response = gen_success_responce("")
    
    return response

# for testing only
def show_info_service():
    total_request_served = "not supported"
    total_hit = "not supported"
    total_miss_rate = "not supported"
    total_hit_rate = "not supported"
    
    # data = get_statistics_from_db()
    # total_request_served = data['total_request_served']
    # total_hit = data['total_hit']
    
    # total_request_served = total_request_served + statistics.num_request_served_5s
    # total_hit = total_hit + statistics.num_hit_5s
    num_item_in_cache = len(config.memcache)
    # if total_request_served != 0:
    #     total_miss_rate = (total_request_served - total_hit) / total_request_served
    #     total_hit_rate = total_hit / total_request_served
    # else:
    #     total_miss_rate = "n/a"
    #     total_hit_rate = "n/a"
    
    
    
    query = ("SELECT num_item_in_cache, used_size, total_request_served, total_hit "
             "FROM status ORDER BY id DESC LIMIT 120;")
    data = db.SQL_command(query)
    num_key_added_10min = statistics.item_added_5s
    used_size_10min = statistics.capacity_used_5s
    request_served_10min = statistics.num_request_served_5s
    num_miss_10min = statistics.num_request_served_5s - statistics.num_hit_5s
    num_hit_10min = statistics.num_hit_5s
    
    for (num_key_added_sql, used_size_sql, request_served_sql, num_hit_sql) in data:
        num_key_added_10min = num_key_added_10min + num_key_added_sql
        used_size_10min = used_size_10min + used_size_sql
        request_served_10min = request_served_10min + request_served_sql
        num_hit_10min = num_hit_10min + num_hit_sql
    if request_served_10min != 0:
        miss_rate_10min = num_miss_10min / request_served_10min
        hit_rate_10min = num_hit_10min / request_served_10min
    else:
        miss_rate_10min = "n/a"
        hit_rate_10min = "n/a"
        
    return render_template("info.html", capacity = config.capacity, replacement_policy = config.replace, \
                           total_num_item_in_cache = num_item_in_cache, total_used_size = statistics.used_size, \
                           total_request_served = total_request_served, total_hit = total_hit, \
                           total_miss_rate = total_miss_rate, total_hit_rate = total_hit_rate, \
                           num_key_added_10min = num_key_added_10min, used_size_10min = used_size_10min, \
                           request_served_10min = request_served_10min, miss_rate_10min = miss_rate_10min, \
                           hit_rate_10min = hit_rate_10min)