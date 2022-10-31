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

from memcache.libs.cloudwatch_lib import my_put_metric_data

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
        statistics.used_size = statistics.used_size - size
        statistics.num_item_in_cache = statistics.num_item_in_cache - 1
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
        statistics.num_item_in_cache = statistics.num_item_in_cache - 1
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
        statistics.num_item_in_cache = statistics.num_item_in_cache - 1
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

def update_database_every_5s():
    try:
        while(config.stop_threads == False):
            utilization = statistics.used_size / config.capacity if config.capacity != 0 else 0

            curr_statistics = {}
            curr_statistics['num_item_in_cache'] = statistics.num_item_in_cache
            curr_statistics['used_size'] = statistics.used_size
            curr_statistics['num_request_served'] = statistics.num_request_served
            curr_statistics['num_GET_request_served'] = statistics.num_GET_request_served
            curr_statistics['num_hit'] = statistics.num_hit
            curr_statistics['num_hit_cloudwatch'] = statistics.num_hit_cloudwatch

            if len(statistics.prev_statistics_every_5s) < 120:
                statistics.prev_statistics_every_5s.append(curr_statistics)
            else:
                statistics.prev_statistics_every_5s.pop(0)
                statistics.prev_statistics_every_5s.append(curr_statistics)
            
            statistics.statistics_10min = {
                'num_item_in_cache' : curr_statistics['num_item_in_cache'] - statistics.prev_statistics_every_5s[0]['num_item_in_cache'],
                'used_size' : curr_statistics['used_size'] - statistics.prev_statistics_every_5s[0]['used_size'],
                'num_request_served' : curr_statistics['num_request_served'] - statistics.prev_statistics_every_5s[0]['num_request_served'],
                'num_GET_request_served' : curr_statistics['num_GET_request_served'] - statistics.prev_statistics_every_5s[0]['num_GET_request_served'],
                'num_hit' : curr_statistics['num_hit'] - statistics.prev_statistics_every_5s[0]['num_hit'],
                'num_hit_cloudwatch' : curr_statistics['num_hit_cloudwatch'] - statistics.prev_statistics_every_5s[0]['num_hit_cloudwatch'],
                'utilization' : utilization
            }
            statistics.statistics_10min['num_miss'] = statistics.statistics_10min['num_GET_request_served'] - statistics.statistics_10min['num_hit_cloudwatch']

            if statistics.statistics_10min['num_GET_request_served'] == 0:
                hit_rate = -1
                miss_rate = -1
            else:
                hit_rate = (statistics.statistics_10min['num_hit_cloudwatch'] / statistics.statistics_10min['num_GET_request_served']) * 100
                miss_rate = 100 - hit_rate

            # insert_5s_statistics_to_db(statistics.statistics_10min['num_item_in_cache'], statistics.statistics_10min['used_size'], \
            #                          statistics.statistics_10min['num_request_served'], statistics.statistics_10min['num_GET_request_served'], \
            #                              statistics.statistics_10min['num_miss'], statistics.statistics_10min['num_hit'], \
            #                                  statistics.statistics_10min['utilization'])
            my_put_metric_data(config.cache_index, 'number of keys added', statistics.statistics_10min['num_item_in_cache'])
            my_put_metric_data(config.cache_index, 'capacity used', statistics.statistics_10min['used_size'])
            my_put_metric_data(config.cache_index, 'request served', statistics.statistics_10min['num_request_served'])
            my_put_metric_data(config.cache_index, 'GET request served', statistics.statistics_10min['num_GET_request_served'])
            my_put_metric_data(config.cache_index, 'number of hit', statistics.statistics_10min['num_hit_cloudwatch'])
            my_put_metric_data(config.cache_index, 'cache utilization', utilization)
            if hit_rate != -1:
                my_put_metric_data(config.cache_index, 'hit rate', hit_rate)
                my_put_metric_data(config.cache_index, 'miss rate', miss_rate)

            # initialize varables every 5s
            time.sleep(5)
    except Exception as error:
        logging.error("background update terminated! {}".format(error))
    return

def file_size(string):
    if "base64," in string:
        data_string = string.split("base64,")[1]
        length = len(data_string) * 3 / 4 - data_string.count("=", -2)
        return length
    else:
        logging.error("file_size - invalid content type: 'base64,' not found, PUT failed")
        return -1