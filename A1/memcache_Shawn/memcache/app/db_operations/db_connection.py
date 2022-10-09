import mysql.connector
import yaml

project_path = __file__.split('memcache_Shawn')[0]
with open(project_path + 'config.yaml') as f:
    db_config = yaml.load(f, Loader=yaml.FullLoader)['database']


def connect_to_db():
    cnx = mysql.connector.connect(user=db_config['user'], password=db_config['password'],
                                  host=db_config['host'],
                                  database=db_config['name'],
                                  auth_plugin='mysql_native_password')
    return cnx
