from flask import Flask

global memcache

webapp = Flask(__name__)
webapp.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
memcache = {}

from app import main