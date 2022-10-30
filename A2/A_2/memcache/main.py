from flask import render_template
from flask import json
import threading

from memcache import webapp
import memcache.config as config
from memcache.libs.cache_operations import get_service, put_service, remove_key_service, \
    refreshConfiguration_service, clear_service, show_info_service, send_stats_service
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

# functions for testting
@webapp.route('/')
def main():
    return render_template("main.html")

@webapp.route('/keys', methods=['GET','POST'])
def show_keys():
    return json.dumps(config.key_list)

@webapp.route('/api/cache/statistics',methods=['POST'])
def show_info():
    return show_info_service()

@webapp.route('/api/cache/statistics',methods=['GET'])
def send_stats():
    return send_stats_service()

# code exicute in the background
# initialize_5s_varables() # legacy code
try:
    thread = threading.Thread(target = update_database_every_5s, daemon = True)
    thread.start()
except:
    config.stop_threads = True
    thread.join()
    print("thread ends")
