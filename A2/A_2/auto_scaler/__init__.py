from flask import Flask

global auto_scaler

webapp = Flask(__name__)

import auto_scaler.main