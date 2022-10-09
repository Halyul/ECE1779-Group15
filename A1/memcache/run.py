#!../venv/bin/python
from memcache.libs.db_operations import config_info
from memcache import webapp
webapp.run(config_info["cache"]["host"],int(config_info["cache"]["port"]),debug=False)