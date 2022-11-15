import threading

from flask import Flask

from . import variables
from .config import STATIC_FOLDER
from .helper_functions.manager_helper import increase_pool_size_manual

global manager_app

webapp = Flask(__name__, static_folder=STATIC_FOLDER)

# Create a memcache node when starting manager
increase_pool_size_manual()


import manager_app.routes



