from flask import Flask

global memcache

webapp = Flask(__name__)

from app import main