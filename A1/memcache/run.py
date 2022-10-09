#!../venv/bin/python
from app.lib.db_operations import config_info
from app import webapp
webapp.run(config_info["cache"]["host"],int(config_info["cache"]["port"]),debug=False)