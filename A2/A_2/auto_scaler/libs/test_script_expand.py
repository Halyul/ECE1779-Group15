import requests
import random
import time
import matplotlib.pyplot as plt

import scaler_test_requests

machine_url = '54.152.136.133'
max_threshold = 0.5

A1_url = 'http://' + machine_url + ':5000'
scaler_test_requests.auto_scaler_url = machine_url
image_path = 'C:/Course Material/UofT/ECE 1779/large image.jpg'

def put_image(key):
    img = {'file': ('large_image.jpg', open(image_path,'rb'), 'image/jpg')}
    response = requests.post(A1_url + '/api/upload', files=img, data={'key': str(key)})
    return response

def get_image(key):
    response = requests.post(A1_url + '/api/key/' + str(key))
    return response

# set auto_scaler to 1MB capacity and auto mode
scaler_test_requests.set_scaler_config(max_threshold, 0.2, 1.5, 0.5, True)
scaler_test_requests.set_scaler_cache_config(1, 'rr')
# print("Waiting for 120s for node bring up...")
# time.sleep(120) # wait arbitry time for cache to run
RW_ratio = 0.5
key_list = []
failed_request = 0
total_get = 0
total_put = 0

num_keys = 20
# write some keys into A1
print("Start writing keys, range of {}".format(num_keys))
for i in range(num_keys):
    # time.sleep(1)
    key = i
    response = put_image(key)
    key_list.append(key)
    if response.status_code != 200:
        failed_request += 1
        print("request {} failed!".format(i))
        continue

time_stamp = []
miss_rate = []
pool_size = []
max_threshold_list = []
pool_size_miss_rate = [-1] * 8
curr_time = 0
print("Start reading keys, range of {}".format(num_keys))
# start reading those keys
for i in range(120):
    time.sleep(10)
    curr_time += 10
    # read
    key = random.choice(key_list)
    response = get_image(key)
    if response.status_code != 200:
        failed_request += 1
        print("request {} failed!".format(i))
        continue
    
    pool_size.append(scaler_test_requests.get_pool_size())
    miss_rate.append(scaler_test_requests.get_miss_rate())
    time_stamp.append(curr_time)
    max_threshold_list.append(max_threshold)
    pool_size_miss_rate[pool_size[-1] - 1] = miss_rate[-1]
    print("request {} done!, pool_size = {}, miss_rate = {}".format(i, pool_size[-1], miss_rate[-1]))


print("\nSimulation done! {} requests failed!".format(failed_request))

plt.plot(time_stamp, pool_size, label = "pool size")
plt.title("Pool Size vs. Time")
plt.ylabel('Pool Size')
plt.xlabel('Time')
plt.savefig("Pool Size vs. Time - expand.jpg")
plt.clf()

plt.plot(time_stamp, miss_rate, label = "miss rate")
plt.plot(time_stamp, max_threshold_list, label = "max threshold")
plt.legend()
plt.title("Miss Rate vs. Time")
plt.ylabel('Miss Rate')
plt.xlabel('Time')
plt.savefig("Miss Rate vs. Time - expand.jpg")
plt.clf()

pool_size_miss_rate_plt = []
x_plt = []
for i in range(8):
    if pool_size_miss_rate[i] != -1:
        pool_size_miss_rate_plt.append(pool_size_miss_rate[i])
        x_plt.append(i+1)

plt.plot(x_plt, pool_size_miss_rate_plt, label = 'miss rate')
plt.plot(x_plt, [max_threshold] * len(x_plt), label = 'max threshold')
plt.legend()
plt.title("Miss Rate vs. Pool Size")
plt.ylabel('Miss Rate')
plt.xlabel('Pool Size')
plt.savefig("Miss Rate vs. Pool Size - expand.jpg")
plt.clf()