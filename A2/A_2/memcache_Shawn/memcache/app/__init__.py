from flask import Flask

from memcache_Shawn.memcache.app.services.helper import create_cache_statistics

webapp = Flask(__name__)

from memcache_Shawn.memcache.app import routes

create_cache_statistics()
