import os
import mysql.connector
from mysql.connector import errorcode
from flask import render_template, url_for, request, redirect
from app import webapp, memcache
from flask import json
import random
import logging
import time
import threading
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# capacity = 1024 * 1024 # default to 1MB
capacity = 3
used_size = 0
replace = 'Least Recently Used'
key_list = [] # list of least recently used keys
stop_threads = False

def initialize_5s_varables():
    global item_added_5s, capacity_used_5s, num_request_served_5s, num_hit_5s
    item_added_5s = 0
    capacity_used_5s= 0
    num_request_served_5s = 0
    num_hit_5s = 0

def update_database_every_5s():
    try:
        while(stop_threads == False):
            # update total statistics
            query = ("SELECT total_request_served, total_hit "
                     "FROM statistics WHERE id = 1;")
            data = SQL_command(query)
            (total_request_served, total_hit) = data[0]
            num_item_in_cache = len(memcache)
            total_request_served = total_request_served + num_request_served_5s
            total_hit = total_hit + num_hit_5s
            if total_request_served != 0:
                miss_rate = (total_request_served - total_hit) / total_request_served
                hit_rate = total_hit / total_request_served
                pre_query = ("UPDATE statistics "
                             "SET num_item_in_cache = {}, used_size = {}, total_request_served = {}, "
                             "total_hit = {}, miss_rate = {}, hit_rate = {} "
                             "WHERE id = 1;")
                query = pre_query.format(num_item_in_cache, used_size, total_request_served, \
                                         total_hit, miss_rate, hit_rate)
            else:
                pre_query = ("UPDATE statistics "
                             "SET num_item_in_cache = {}, used_size = {}, total_request_served = {}, "
                             "total_hit = {} "
                             "WHERE id = 1;")
                query = pre_query.format(num_item_in_cache, used_size, total_request_served, \
                                         total_hit)
            SQL_command(query)
            
            # update statistics for last 5s (this table will be used for 'last 10min statistics')
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            prev_time = now - timedelta(minutes = 10)
            prev_time = prev_time.strftime("%Y-%m-%d %H:%M:%S")
            pre_query = ("DELETE FROM statistics_10min WHERE time < \'{}\'; ")
            query = pre_query.format(prev_time)
            SQL_command(query)
            pre_query = ("INSERT INTO statistics_10min (time, num_item_added, capacity_used, num_request_served, num_miss, num_hit) "
                         "VALUES (\'{}\', {}, {}, {}, {}, {});")
            query = pre_query.format(current_time, item_added_5s, capacity_used_5s, \
                                     num_request_served_5s, num_request_served_5s - num_hit_5s, num_hit_5s)
            SQL_command(query)
            
            # initialize varables every 5s
            initialize_5s_varables()
            time.sleep(5)
    except:
        print("end")
    return

def SQL_command(command):
    # setup SQL access
    try:
        cnx = mysql.connector.connect(user='root', password='my_SQL_password',
                                      host='127.0.0.1',
                                      database='ece1779_memcache')
        cursor = cnx.cursor()
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return
    else:
        query = command  
        # print(query)
        
        cursor.execute(query)
        out_data = cursor.fetchall()
        
        cnx.commit()
        cursor.close()
        cnx.close()
        return out_data

def gen_failed_responce(code, message):
    json_response = {
        "success": "false",
        "error": {
            "code": code,
            "message": message
             }
    }
    response = webapp.response_class(
        response=json.dumps(json_response),
        status=400,
        mimetype='application/json'
    )
    return response

# def allowed_file(filename):
#     if ('.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS):
#         return True
#     return False

@webapp.route('/')
def main():
    return render_template("main.html")

@webapp.route('/api/cache/key',methods=['POST'])
def get():
    global num_request_served_5s, num_hit_5s
    key = request.form.get('key')

    if key in memcache:
        value = memcache[key]
        # lest recently used key will be in index 0
        key_list.remove(key) # remove it from the list
        key_list.append(key) # add it to the end of the list
        num_hit_5s = num_hit_5s + 1
        
        json_response = {
            "success": "true",
            "content" : value
        }
        response = webapp.response_class(
            response=json.dumps(json_response),
            status=200,
            mimetype='application/json'
        )
    else:
        response = gen_failed_responce(400, "Unknown key")
    
    num_request_served_5s = num_request_served_5s + 1
    
    return response

@webapp.route('/api/cache/content',methods=['POST'])
def put():
    # check if there is a key
    if request.form.get('key') == '':
        response = gen_failed_responce(400, "Missing key")
        return response
    # check if there is a value
    if request.form.get('value') == '':
        response = gen_failed_responce(400, "Missing value")
        return response
    
    # when there is a image been submitted proeprly
    key = request.form.get('key')
    value = request.form.get('value')
    # space check
    global used_size, item_added_5s, capacity_used_5s
    if len(value) > capacity:
        response = gen_failed_responce(400, "File is bigger then the whole cache")
        return response
    # if free space is not enough, do some replacement until cache is empty or having enough space
    if used_size + len(value) > capacity: 
        while len(memcache) > 0 and used_size + len(value) > capacity:
            remove_element()
    # once we have enough free space, save the file into the cache
    memcache[key] = value
    used_size = used_size + len(value)
    # added to key_list to keep track of which one is been recently used
    if key in key_list:
        key_list.remove(key) # remove it from the list
        key_list.append(key) # add it to the end of the list
    else:
        key_list.append(key) # add it to the end of the list
    item_added_5s = item_added_5s + 1
    capacity_used_5s = capacity_used_5s + len(value)
    
    logging.debug('put - key: ' + key + ' with len(value) of ' + str(len(value)) + ' added to the cache')
    logging.info('put - cache used = ' + str(used_size))
        
    # make the correct response
    json_response = {
        "success": "true"
    }
    response = webapp.response_class(
        response=json.dumps(json_response),
        status=200,
        mimetype='application/json'
    )
    return response

def remove_element():
    global used_size, capacity_used_5s
    if replace == 'Random':
        (key, value) = random.choice(list(memcache.items()))
        del memcache[key]
        key_list.remove(key)
        used_size = used_size - len(value)
        capacity_used_5s = capacity_used_5s - len(value)
        logging.debug('remove_element - replace policy is ' + replace)
        logging.debug('remove_element - key: ' + key + ' with len(value) of ' + str(len(value)) + ' removed from the cache')
        logging.info('remove_element - cache used = ' + str(used_size))
        return
    elif replace == 'Least Recently Used':
        key = key_list[0]
        value = memcache[key]
        del memcache[key]
        key_list.remove(key)
        used_size = used_size - len(value)
        capacity_used_5s = capacity_used_5s - len(value)
        logging.debug('remove_element - replace policy is ' + replace)
        logging.debug('remove_element - key: ' + key + ' with len(value) of ' + str(len(value)) + ' removed from the cache')
        logging.info('remove_element - cache used = ' + str(used_size))
        return
    else:
        logging.error('remove_element - Invaild replace policy: ' + replace)
        exit()

def set_parameters(new_capacity, new_replace):
    global capacity, replace
    capacity = new_capacity * 1024 * 1024
    # if used space is more then the new capacity, remove elements until used space is small enough
    while used_size > capacity:
        remove_element()
    # check if the replace policy is valid or not
    if new_replace in ['Random', 'Least Recently Used']:
        replace = new_replace
    else:
        response = gen_failed_responce(400, "Invalid replace policy")
        return response
    return

# remove key, key will be passed from the from
@webapp.route('/api/cache/key', methods=['DELETE'])
def remove_key():
    key = request.form.get('key')
    if key in memcache:
        invalidateKey(key)
    return redirect(url_for('show_keys'))

# remove key, key will be passed by the argument
def invalidateKey(key):
    global capacity_used_5s, used_size
    if key in key_list:
        value = memcache[key]
        capacity_used_5s = capacity_used_5s - len(value)
        used_size = used_size - len(value)
        del memcache[key]
        key_list.remove(key)
    else:
        logging.warning('invalidateKey - key: ' + key + ' is not in the cache')
    return

# to read mem-cache related details from the database and reconfigure it based 
# on the values set by the user
@webapp.route('/api/cache/config',methods=['GET'])
def refreshConfiguration():
    query = ("SELECT capacity, replacement_policy FROM memcache_config "
             "WHERE id = 1;")
    data = SQL_command(query)
    (new_capacity, new_replacement_policy) = data[0]
    set_parameters(new_capacity, new_replacement_policy)
    
    # make the correct response
    json_response = {
        "success": "true"
    }
    response = webapp.response_class(
        response=json.dumps(json_response),
        status=200,
        mimetype='application/json'
    )
    
    return response

# just for testing
@webapp.route('/keys', methods=['GET','POST'])
def show_keys():
    return json.dumps(key_list)

@webapp.route('/api/cache',methods=['DELETE'])
def CLEAR():
    global memcache, used_size, key_list, capacity_used_5s
    memcache = {}
    key_list = []
    capacity_used_5s = capacity_used_5s - used_size
    used_size = 0
    logging.debug('CLEAR - cache cleared')
    
    # make the correct response
    json_response = {
        "success": "true"
    }
    response = webapp.response_class(
        response=json.dumps(json_response),
        status=200,
        mimetype='application/json'
    )
    
    return response

@webapp.route('/api/cache/statistics',methods=['GET'])
def show_info():
    query = ("SELECT total_request_served, total_hit "
             "FROM statistics WHERE id = 1;")
    data = SQL_command(query)
    (total_request_served, total_hit) = data[0]
    total_request_served = total_request_served + num_request_served_5s
    total_hit = total_hit + num_hit_5s
    num_item_in_cache = len(memcache)
    if total_request_served != 0:
        total_miss_rate = (total_request_served - total_hit) / total_request_served
        total_hit_rate = total_hit / total_request_served
    else:
        total_miss_rate = "n/a"
        total_hit_rate = "n/a"
    
    query = ("SELECT num_item_added, capacity_used, num_request_served, num_miss, num_hit "
             "FROM statistics_10min;")
    data = SQL_command(query)
    num_key_added_10min = item_added_5s
    used_size_10min = capacity_used_5s
    request_served_10min = num_request_served_5s
    num_miss_10min = num_request_served_5s - num_hit_5s
    num_hit_10min = num_hit_5s
    for (num_key_added_sql, used_size_sql, request_served_sql, num_miss_sql, num_hit_sql) in data:
        num_key_added_10min = num_key_added_10min + num_key_added_sql
        used_size_10min = used_size_10min + used_size_sql
        request_served_10min = request_served_10min + request_served_sql
        num_miss_10min = num_miss_10min + num_miss_sql
        num_hit_10min = num_hit_10min + num_hit_sql
    if request_served_10min != 0:
        miss_rate_10min = num_miss_10min / request_served_10min
        hit_rate_10min = num_hit_10min / request_served_10min
    else:
        miss_rate_10min = "n/a"
        hit_rate_10min = "n/a"
        
    return render_template("info.html", capacity = capacity, replacement_policy = replace, \
                           total_num_item_in_cache = num_item_in_cache, total_used_size = used_size, \
                           total_request_served = total_request_served, total_hit = total_hit, \
                           total_miss_rate = total_miss_rate, total_hit_rate = total_hit_rate, \
                           num_key_added_10min = num_key_added_10min, used_size_10min = used_size_10min, \
                           request_served_10min = request_served_10min, miss_rate_10min = miss_rate_10min, \
                           hit_rate_10min = hit_rate_10min)

# code exicute in the beginning
initialize_5s_varables()
try:
    thread = threading.Thread(target = update_database_every_5s, daemon = True)
    thread.start()
except:
    stop_threads = True
    thread.join()
    print("thread ends")