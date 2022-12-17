from flask_cors import CORS
from flask import Flask

global album

webapp = Flask(__name__)
CORS(webapp)


import album.routes
