from flask import render_template, redirect, url_for, request
import threading

from auto_scaler import webapp
import auto_scaler.config as config
import auto_scaler.statistics as statistics
from auto_scaler.libs.scaler_operations import responce_main, responce_refresh_config, \
    responce_terminate_all, responce_list_cache, check_miss_rate_every_min, responce_get_node_list, \
    responce_set_node_list, responce_do_node_delete, responce_refresh_cache_config
from auto_scaler.libs.scaler_support_func import initialization

@webapp.route('/',methods=['GET'])
def home():
    return redirect(url_for('main'))

@webapp.route('/api/scaler/',methods=['GET'])
def main():
    return responce_main()

@webapp.route('/api/scaler/config',methods=['POST'])
def refresh_config():
    return responce_refresh_config()

@webapp.route('/api/scaler/cache_config',methods=['POST'])
def refresh_cache_config():
    return responce_refresh_cache_config()

@webapp.route('/api/scaler/cache_list',methods=['GET'])
def get_node_list():
    return responce_get_node_list()

@webapp.route('/api/scaler/cache_list',methods=['POST'])
def set_node_list():
    return responce_set_node_list()

@webapp.route('/api/poolsize/change',methods=['POST'])
def do_node_delete():
    return responce_do_node_delete()

# for testing
@webapp.route('/api/scaler/terminate_all',methods=['POST'])
def terminate_all():
    return responce_terminate_all()

# for testing
@webapp.route('/api/scaler/list',methods=['GET', 'POST'])
def list_cache():
    return responce_list_cache()

# for testing
@webapp.route('/api/scaler/set_test_miss_rate',methods=['POST'])
def set_test_miss_rate():
    statistics.test_miss_rate = float(request.form.get('test_miss_rate'))
    check_miss_rate_every_min(manully_triggered = True)
    return redirect(url_for('main'))

initialization()
thread = threading.Thread(target = check_miss_rate_every_min, daemon = True)
# code exicute in the background
try:
    # pass
    thread.start()
except:
    config.stop_threads = True
    thread.join()
    print("thread ends")
