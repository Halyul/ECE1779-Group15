
from flask import Flask
from .config import STATIC_FOLDER
global manager_app

webapp = Flask(__name__, static_folder=STATIC_FOLDER)

import manager_app.routes



