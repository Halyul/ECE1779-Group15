import mysql.connector
from flask import Flask

from app.services.helper import create_cache_statistics

webapp = Flask(__name__)

# Add Database
cnx = mysql.connector.connect(user='root', password='password123',
                              host='127.0.0.1',
                              database='memcache_db',
                              auth_plugin='mysql_native_password')

cursor = cnx.cursor(buffered=True)

from app import routes

create_cache_statistics()
