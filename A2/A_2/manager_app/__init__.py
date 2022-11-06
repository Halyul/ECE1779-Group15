from flask import Flask

global manager_app

webapp = Flask(__name__)

data_30_min = []
resize_pool_option = 'manual'
resize_pool_parameters = {}
