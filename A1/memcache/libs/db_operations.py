import libs.db_lib
import sys
import pathlib

sys.path.append("..") 
import server.config

# read the setup config from the yaml file
setup_config = server.config.Config()
config_info = setup_config.fetch()

# setup the my_db object with the correct database parameters
# db = db_lib.my_db('root', 'my_SQL_password', '127.0.0.1', 'ece1779_memcache')
db = libs.db_lib.my_db(config_info['database']['user'], config_info['database']['password'], \
                  config_info['database']['host'], config_info['database']['name'])

def get_config_from_db():
    data = {}
    data['capacity'] = db.get_from_table(config_info['database']["table_names"]['config'], '`value`', "`key` = 'capacity'")[0][0]
    data['capacity'] = int(data['capacity'])
    data['policy'] = db.get_from_table(config_info['database']["table_names"]['config'], '`value`', "`key` = 'policy'")[0][0]
    return data

# def get_statistics_from_db():
#     data = {}
#     data['total_request_served'] = db.get_from_table(config_info['database']["table_names"]['status'], 'total_request_served', "id = 1")[0][0]
#     data['total_hit'] = db.get_from_table(config_info['database']["table_names"]['status'], 'total_hit', "id = 1")[0][0]
#     return data

# def get_5s_statistics_from_db():
#     data = {}
#     data['num_key_added_10min'] = db.get_from_table('statistics_10min', 'num_item_added')[0][0]
#     data['used_size_10min'] = db.get_from_table('statistics_10min', 'capacity_used')[0][0]
#     data['request_served_10min'] = db.get_from_table('statistics_10min', 'num_request_served')[0][0]
#     data['num_miss_10min'] = db.get_from_table('statistics_10min', 'num_miss')[0][0]
#     data['num_hit_10min'] = db.get_from_table('statistics_10min', 'num_hit')[0][0]
#     return data

def insert_5s_statistics_to_db(item_added_5s, capacity_used_5s, num_request_served_5s, num_miss_5s, num_hit_5s):
    if num_request_served_5s != 0:
        command = ("INSERT INTO {} (num_item_in_cache, used_size, total_request_served, total_hit, miss_rate, hit_rate) "
                             "VALUES ({}, {}, {}, {}, {}, {});").format(config_info['database']["table_names"]['status'], \
                                                                            item_added_5s, \
                                                                            capacity_used_5s, \
                                                                                num_request_served_5s, \
                                                                                    num_hit_5s, num_miss_5s / num_request_served_5s, \
                                                                                        num_hit_5s / num_request_served_5s)
    else:
        command = ("INSERT INTO {} (num_item_in_cache, used_size, total_request_served, total_hit) "
                             "VALUES ({}, {}, {}, {});").format(config_info['database']["table_names"]['status'], \
                                                                            item_added_5s, \
                                                                            capacity_used_5s, \
                                                                                num_request_served_5s, \
                                                                                    num_hit_5s)
    db.SQL_command(command)
    return

# def delete_5s_statistics_from_db(time_list):
#     command = "DELETE FROM {} WHERE time < \'{}\'; ".format(config_info['database']["table_names"]['status'], time_list)
#     db.SQL_command(command)
#     return