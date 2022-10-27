import os
from flask import Flask, jsonify, send_from_directory, make_response
from flask_restful import Api as RestfulApi
from flask_cors import CORS
from server.message import errorhandler
from server.api import Api
from server.config import Config

CONFIG = Config().fetch()

APP = Flask(__name__, static_folder=CONFIG["server"]["static_folder"])
CORS(APP)
APIAPP = RestfulApi(APP)

@APP.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(errorhandler(400)), 400)

@APP.errorhandler(404)
def not_found(error):
    return make_response(jsonify(errorhandler(404)), 404)

@APP.errorhandler(500)
def server_error(error):
    return make_response(jsonify(errorhandler(500)), 500)

@APP.route("/", defaults={"path": ""})
@APP.route("/<path:path>")
def serve(path):
    def set_mimetype(filename: str):
        if filename.endswith("js"):
            return "text/javascript"
        elif filename.endswith("css"):
            return "text/css"
        elif filename.endswith("svg"):
            return "image/svg+xml"

    if path != "" and os.path.exists(APP.static_folder + "/" + path):
        return send_from_directory(
            APP.static_folder, 
            path,
            mimetype=set_mimetype(path)
        )
    else:
        return send_from_directory(APP.static_folder, "index.html")

APIAPP.add_resource(Api, 
    '/api/upload',
    '/api/list_keys',
    '/api/key/<key>',
    '/api/config',
    '/api/status',
)

if __name__ == '__main__':
    APP.run(host=CONFIG["server"]["host"], port=CONFIG["server"]["port"], debug=CONFIG["server"]["debug"])
