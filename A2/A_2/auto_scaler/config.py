import logging

import sys
sys.path.append("..") 
import server.config

logging.basicConfig(level=logging.INFO)
max_miss_rate_threshold = 0.6
min_miss_rate_threshold = 0.4
expand_ratio = 1.5
shrink_ratio = 1.5

cache_pool_size = 0 # size can be from 1 to 8
cache_pool_ids = [] # keeps a list of ids, can be used to look up the ip address, or find out the cache node index

auto_mode = True

stop_threads = False

# cache config
capacity = 1 # in MB
replacement_policy = 'rr'

# read the setup config from the yaml file
setup_config = server.config.Config()
config_info = setup_config.fetch()
cache_port = config_info['cache']['port']

# aws configs
ami_id = config_info['aws']['ami_id']
subnet_id = config_info['aws']['subnet_id']
security_group_id = config_info['aws']['security_group_id']
ssh_key_name = config_info['aws']['ssh_key_name']
private_key_file = config_info['aws']['private_key_file']

# github
github_access_token = config_info['github']['access_token']