import logging

import sys
sys.path.append("..") 
import server.config

logging.basicConfig(level=logging.ERROR)
max_miss_rate_threshold = 0.8
min_miss_rate_threshold = 0.4
expand_ratio = 1.5
shrink_ratio = 1.5

cache_pool_size = 0 # size can be from 1 to 8
cache_pool_ids = []

auto_mode = True

stop_threads = False

# read the setup config from the yaml file
setup_config = server.config.Config()
config_info = setup_config.fetch()
cache_port = config_info['cache']['port']

# aws configs
ami_id = 'ami-0a1a1906efbd4c711'
subnet_id = 'subnet-005acfeb3976436cd'
security_group_id = 'sg-0b51a4f8399515236'