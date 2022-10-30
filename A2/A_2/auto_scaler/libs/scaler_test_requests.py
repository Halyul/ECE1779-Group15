import requests
import json

# TODO: need to read it from the yaml
port = 5001

def set_scaler_config(max_miss_rate_threshold, min_miss_rate_threshold, expand_ratio, shrink_ratio, auto_mode):
    passed_data=[('max_miss_rate_threshold', max_miss_rate_threshold), ('min_miss_rate_threshold', min_miss_rate_threshold), \
        ('expand_ratio', expand_ratio), ('shrink_ratio', shrink_ratio), ('auto_mode', auto_mode)]
    response = requests.post('http://127.0.0.1:' + str(port) + '/api/scaler/config', data=passed_data)
    return response.content

def set_test_miss_rate(test_miss_rate):
    passed_data=[('test_miss_rate', test_miss_rate)]
    response = requests.post('http://127.0.0.1:' + str(port) + '/api/scaler/set_test_miss_rate', data=passed_data)
    return response.content