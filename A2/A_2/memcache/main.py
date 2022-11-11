from flask import render_template, request
from flask import json
import threading
import logging

from memcache import webapp
import memcache.config as config
import memcache.statistics as statistics
from memcache.libs.cache_operations import get_service, put_service, remove_key_service, \
    refreshConfiguration_service, clear_service, show_info_service, send_stats_service, clear_stats_service, \
    move_keys_to_other_nodes_service
from memcache.libs.cache_support_func import update_database_every_5s

@webapp.route('/api/cache/key',methods=['POST'])
def get():
    return get_service()

@webapp.route('/api/cache/content',methods=['POST'])
def put():
    return put_service()

@webapp.route('/api/cache/key', methods=['DELETE'])
def remove_key():
    return remove_key_service()

@webapp.route('/api/cache/config',methods=['POST'])
def refreshConfiguration():
    return refreshConfiguration_service()

@webapp.route('/api/cache',methods=['DELETE'])
def CLEAR():
    return clear_service()

@webapp.route('/api/cache/statistics',methods=['GET'])
def send_stats():
    return send_stats_service()

@webapp.route('/api/cache/statistics',methods=['DELETE'])
def clear_stats():
    return clear_stats_service()

@webapp.route('/api/cache/move_keys',methods=['POST'])
def move_keys_to_other_nodes():
    return move_keys_to_other_nodes_service()

# this is used to make the master node (node 0) have the num_hit of the whole pool
# and slave nodes will have num_hit equals to 0 once master node has its num_hit updated
@webapp.route('/api/cache/set_num_hit',methods=['POST'])
def set_num_hit():
    statistics.num_hit = int(request.form.get('num_hit'))
    return "cache node {} statistics.num_hit = {}".format(config.cache_index, statistics.num_hit)

# functions for testting
@webapp.route('/')
def main():
    source_ip = request.environ['REMOTE_ADDR']
    logging.info("main page - source ip is {}".format(source_ip))
    return render_template("main.html")

@webapp.route('/keys', methods=['GET','POST'])
def show_keys():
    return json.dumps(config.key_list)

@webapp.route('/api/cache/statistics',methods=['POST'])
def show_info():
    return show_info_service()

# code exicute in the background
# initialize_5s_varables() # legacy code
try:
    thread = threading.Thread(target = update_database_every_5s, daemon = True)
    thread.start()
except:
    config.stop_threads = True
    thread.join()
    print("thread ends")
