import requests
import json

import sys
sys.path.append(".") 
import server.config

setup_config = server.config.Config()
config_info = setup_config.fetch()

auto_scaler_url = '127.0.0.1'
port = config_info['auto_scaler']['port']

def set_scaler_config(max_miss_rate_threshold, min_miss_rate_threshold, expand_ratio, shrink_ratio, auto_mode):
    passed_data=[('max_miss_rate_threshold', max_miss_rate_threshold), ('min_miss_rate_threshold', min_miss_rate_threshold), \
        ('ratio_expand_pool', expand_ratio), ('ratio_shrink_pool', shrink_ratio), ('auto_mode', auto_mode)]
    response = requests.post('http://' + auto_scaler_url + ':' + str(port) + '/api/scaler/config', data=passed_data)
    return response.content

def set_scaler_cache_config(capacity, replacement_policy):
    passed_data=[('capacity', capacity), ('replacement_policy', replacement_policy)]
    response = requests.post('http://' + auto_scaler_url + ':' + str(port) + '/api/scaler/cache_config', data=passed_data)
    return response.content

def set_test_miss_rate(test_miss_rate):
    passed_data=[('test_miss_rate', test_miss_rate)]
    response = requests.post('http://' + auto_scaler_url + ':' + str(port) + '/api/scaler/set_test_miss_rate', data=passed_data)
    return response.content

def delete_node(ip):
    passed_data=[('cache_ip', ip)]
    response = requests.post('http://' + auto_scaler_url + ':' + str(port) + '/api/poolsize/change', data=passed_data)
    return response.content

def get_node_list():
    response = requests.get('http://' + auto_scaler_url + ':' + str(port) + '/api/scaler/cache_list')
    return response.content

def set_node_list(node_list):
    passed_data={'cache_pool_ids': node_list}
    response = requests.post('http://' + auto_scaler_url + ':' + str(port) + '/api/scaler/cache_list', json=passed_data)
    return response.content

def test_delete_node(cache_ip):
    target_ip = '3.86.213.92'
    # dict = json.dumps({'port': '5010', 'dest': {target_ip: ['a', 'c']}})
    port = '5010'
    dest = json.dumps({})
    response = requests.post('http://' + cache_ip + ':5001' + '/api/cache/move_keys', data=[('port', port), ('dest', dest)])
    return response.content

def get_pool_size():
    response = requests.post('http://' + auto_scaler_url + ':' + str(port) + '/api/scaler/pool_size')
    return int(response.content)

def get_miss_rate():
    response = requests.post('http://' + auto_scaler_url + ':' + str(port) + '/api/scaler/miss_rate')
    try:
        return float(response.content)
    except:
        return 0