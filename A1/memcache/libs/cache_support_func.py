from flask import json
import logging
import random
from datetime import datetime, timedelta
import time

import sys
sys.path.append("../..") 
from memcache import webapp
import memcache.config as config
import memcache.statistics as statistics

from memcache.libs.db_operations import db, insert_5s_statistics_to_db, config_info

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

# remove key, key will be passed by the argument
def invalidateKey(key):
    if key in config.key_list:
        value = config.memcache[key]
        size = file_size(value)
        statistics.capacity_used_5s = statistics.capacity_used_5s - size
        statistics.used_size = statistics.used_size - size
        del config.memcache[key]
        config.key_list.remove(key)
    else:
        logging.warning('invalidateKey - key: ' + key + ' is not in the cache')
    return

def remove_element():
    if config.replace == 'rr':
        (key, value) = random.choice(list(config.memcache.items()))
        del config.memcache[key]
        config.key_list.remove(key)
        size = file_size(value)
        statistics.used_size = statistics.used_size - size
        statistics.capacity_used_5s = statistics.capacity_used_5s - size
        logging.debug('remove_element - replace policy is ' + config.replace)
        logging.debug('remove_element - key: ' + key + ' with len(value) of ' + str(size) + ' removed from the cache')
        logging.info('remove_element - cache used = ' + str(statistics.used_size))
        return
    elif config.replace == 'lru':
        key = config.key_list[0]
        value = config.memcache[key]
        del config.memcache[key]
        config.key_list.remove(key)
        size = file_size(value)
        statistics.used_size = statistics.used_size - size
        statistics.capacity_used_5s = statistics.capacity_used_5s - size
        logging.debug('remove_element - replace policy is ' + config.replace)
        logging.debug('remove_element - key: ' + key + ' with len(value) of ' + str(size) + ' removed from the cache')
        logging.info('remove_element - cache used = ' + str(statistics.used_size))
        return
    else:
        logging.error('remove_element - Invaild replace policy: ' + config.replace)
        exit()

def set_parameters(new_config, new_replace):
    config.capacity = new_config * 1024 * 1024
    # if used space is more then the new config.capacity, remove elements until used space is small enough
    while statistics.used_size > config.capacity:
        remove_element()
    # check if the replace policy is valid or not
    if new_replace in ['rr', 'lru']:
        config.replace = new_replace
        return (200, '')
    else:
        return (400, "Invalid replace policy")
    return

def initialize_5s_varables():
    statistics.item_added_5s = 0
    statistics.capacity_used_5s= 0
    statistics.num_request_served_5s = 0
    statistics.num_GET_request_served_5s = 0
    statistics.num_hit_5s = 0

def update_database_every_5s():
    try:
        while(config.stop_threads == False):
            # data = get_statistics_from_db()
            # total_request_served = data['total_request_served']
            # total_hit = data['total_hit']
            
            # num_item_in_cache = len(config.memcache)
            # total_request_served = total_request_served + statistics.num_request_served_5s
            # total_hit = total_hit + statistics.num_hit_5s
            # if total_request_served != 0:
            #     miss_rate = (total_request_served - total_hit) / total_request_served
            #     hit_rate = total_hit / total_request_served
            #     pre_query = ("UPDATE {} "
            #                  "SET num_item_in_cache = {}, used_size = {}, total_request_served = {}, "
            #                  "total_hit = {}, miss_rate = {}, hit_rate = {} "
            #                  "WHERE id = 1;")
            #     query = pre_query.format(config_info['database']["table_names"]['status'], num_item_in_cache, statistics.used_size, total_request_served, \
            #                              total_hit, miss_rate, hit_rate)
            # else:
            #     pre_query = ("UPDATE {} "
            #                  "SET num_item_in_cache = {}, used_size = {}, total_request_served = {}, "
            #                  "total_hit = {} "
            #                  "WHERE id = 1;")
            #     query = pre_query.format(config_info['database']["table_names"]['status'] ,num_item_in_cache, statistics.used_size, total_request_served, \
            #                              total_hit)
            # db.SQL_command(query)
            
            # update statistics for last 5s (this table will be used for 'last 10min statistics')
            # now = datetime.now()
            # current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            # prev_time = now - timedelta(minutes = 10)
            # prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")
            
            # delete_5s_statistics_from_db(prev_time)
            
            # pre_query = ("INSERT INTO statistics_10min (time, num_item_added, capacity_used, num_request_served, num_miss, num_hit) "
            #              "VALUES (\'{}\', {}, {}, {}, {}, {});")
            # query = pre_query.format(current_time, statistics.item_added_5s, statistics.capacity_used_5s, \
            #                          statistics.num_request_served_5s, statistics.num_request_served_5s - statistics.num_hit_5s, statistics.num_hit_5s)
            # SQL_command(query)
            
            utilization = statistics.used_size / config.capacity
            insert_5s_statistics_to_db(statistics.item_added_5s, statistics.capacity_used_5s, \
                                     statistics.num_request_served_5s, statistics.num_GET_request_served_5s, \
                                         statistics.num_GET_request_served_5s - statistics.num_hit_5s, statistics.num_hit_5s, \
                                             utilization)
            
            # initialize varables every 5s
            initialize_5s_varables()
            time.sleep(5)
    except Exception as error:
        print(error)
        print("background update terminated")
    return

def file_size(string):
    if "base64," in string:
        data_string = string.split("base64,")[1]
        length = len(data_string) * 3 / 4 - data_string.count("=", -2)
        return length
    else:
        logging.ERROR("file_size - invalid content type: 'base64,' not found, size calculation will be incorrect")
        return -1