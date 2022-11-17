import requests
import random
import time

import scaler_test_requests

A1_url = 'http://127.0.0.1:5000'
scaler_test_requests.auto_scaler_url = '127.0.0.1'
image_path = 'C:/Course Material/UofT/ECE 1779/large image.jpg'

def put_image(key):
    img = {'file': ('large_image.jpg', open(image_path,'rb'), 'image/jpg')}
    response = requests.post(A1_url + '/api/upload', files=img, data={'key': str(key)})
    return response

def get_image(key):
    response = requests.post(A1_url + '/api/key/' + str(key))
    return response

# set auto_scaler to 1MB capacity and auto mode
scaler_test_requests.set_scaler_cache_config(1, 'rr')
scaler_test_requests.set_scaler_config(0.5, 0, 1.5, 0.5, True)
time.sleep(120) # wait arbitry time for cache to run
RW_ratio = 0.5
key_list = []
failed_request = 0
total_get = 0
total_put = 0

list_miss_rate = [[]] * 8

for i in range(120):
    if i == 0:
        # write
        key = random.randrange(20)
        response = put_image(key)
        key_list.append(key)
        if response.status_code != 200:
            failed_request += 1
            continue
        total_put += 1
    else:
        if random.random() > RW_ratio:
            # write
            key = random.randrange(20)
            response = put_image(key)
            key_list.append(key)
            if response.status_code != 200:
                failed_request += 1
                continue
            total_put += 1
        else:
            # read
            key = random.choice(key_list)
            response = get_image(key)
            if response.status_code != 200:
                failed_request += 1
                continue
            total_get += 1

    pool_size = scaler_test_requests.get_pool_size()
    list_miss_rate[pool_size].append(scaler_test_requests.get_miss_rate())
    time.sleep(5)


print("Simulation done! {} requests failed!".format(failed_request))
print("Served {} get request, {} put request.".format(total_get, total_put))
print("list_miss_rate = {}".format(list_miss_rate))