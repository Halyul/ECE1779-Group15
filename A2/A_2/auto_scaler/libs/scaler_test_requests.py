import requests
import json

# TODO: need to read it from the yaml
port = 5010

def set_scaler_config(max_miss_rate_threshold, min_miss_rate_threshold, expand_ratio, shrink_ratio, auto_mode):
    passed_data=[('max_miss_rate_threshold', max_miss_rate_threshold), ('min_miss_rate_threshold', min_miss_rate_threshold), \
        ('expand_ratio', expand_ratio), ('shrink_ratio', shrink_ratio), ('auto_mode', auto_mode)]
    response = requests.post('http://127.0.0.1:' + str(port) + '/api/scaler/config', data=passed_data)
    return response.content

def set_scaler_cache_config(capacity, replacement_policy):
    passed_data=[('capacity', capacity), ('replacement_policy', replacement_policy)]
    response = requests.post('http://127.0.0.1:' + str(port) + '/api/scaler/cache_config', data=passed_data)
    return response.content

def set_test_miss_rate(test_miss_rate):
    passed_data=[('test_miss_rate', test_miss_rate)]
    response = requests.post('http://127.0.0.1:' + str(port) + '/api/scaler/set_test_miss_rate', data=passed_data)
    return response.content

def delete_node(ip):
    passed_data=[('cache_ip', ip)]
    response = requests.post('http://127.0.0.1:' + str(port) + '/api/poolsize/change', data=passed_data)
    return response.content

def get_node_list():
    response = requests.get('http://127.0.0.1:' + str(port) + '/api/scaler/cache_list')
    return response.content

def set_node_list(node_list):
    passed_data=[('cache_pool_ids', json.dumps(node_list))]
    response = requests.post('http://127.0.0.1:' + str(port) + '/api/scaler/cache_list', data=passed_data)
    return response.content

def test_delete_node(cache_ip):
    target_ip = '3.86.213.92'
    # dict = json.dumps({'port': '5010', 'dest': {target_ip: ['a', 'c']}})
    port = '5010'
    dest = json.dumps({})
    response = requests.post('http://' + cache_ip + ':5001' + '/api/cache/move_keys', data=[('port', port), ('dest', dest)])