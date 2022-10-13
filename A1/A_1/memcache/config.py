import logging

logging.basicConfig(level=logging.DEBUG)
# capacity = 1024 * 1024 # default to 1MB
capacity = 3
replace = 'lru'

memcache = {}
key_list = [] # list of least recently used keys
stop_threads = False