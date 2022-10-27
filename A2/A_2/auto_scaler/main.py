from flask import render_template, redirect, url_for
import threading

from auto_scaler import webapp
import auto_scaler.config as config
from auto_scaler.libs.scaler_operations import responce_main, responce_refresh_config, \
    responce_terminate_all, responce_list_cache, check_miss_rate_every_min
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

# for testing
@webapp.route('/api/scaler/terminate_all',methods=['POST'])
def terminate_all():
    return responce_terminate_all()

# for testing
@webapp.route('/api/scaler/list',methods=['GET', 'POST'])
def list_cache():
    return responce_list_cache()

# initialization()
# code exicute in the background
try:
    thread = threading.Thread(target = check_miss_rate_every_min, daemon = True)
    # thread.start()
except:
    config.stop_threads = True
    thread.join()
    print("thread ends")
