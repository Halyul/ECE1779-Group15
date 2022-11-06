import logging

logging.basicConfig(level=logging.INFO, filemode='w', filename='cache.log')
# logging.basicConfig(level=logging.INFO)

# capacity = 1024 * 1024 # default to 1MB
capacity = 3
replace = 'lru'

memcache = {}
key_list = [] # list of least recently used keys
stop_threads = False

cache_index = 0 # used to distinguish different cache nodes on CloudWatch, takes value from 0-7