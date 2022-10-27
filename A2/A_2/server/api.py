import werkzeug.datastructures
from flask_restful import Resource, reqparse, request
from .message import response
from .routes.status import status
from .routes.config import get_config, set_config
from .routes.key import create_key, get_key, list_keys

PARASER = reqparse.RequestParser()

class Api(Resource):

    def __init__(self):
        self.key = None

    @response
    def get(self):
        urls = [
            "/api/config",
            "/api/status",
        ]
        path = request.path
        if path not in urls:
            return False, 400, None
        destination = path.split("/")[2]
        if destination == "config":
            return get_config()
        if destination == "status":
            return status()

    @response
    def post(self, key=None):
        urls = [
            "/api/upload",
            "/api/list_keys",
            "/api/config",
            "/api/key/{}".format(key),
        ]
        path = request.path
        if path not in urls:
            return False, 400, None
        parser = reqparse.RequestParser()
        destination = path.split("/")[2]
        if destination == "upload":
            parser.add_argument("key", type=str, location="form", required=True)
            parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location="files", required=True)
            args = parser.parse_args()
            return create_key(args)
        if destination == "key":
            return get_key(key)
        if destination == "list_keys":
            return list_keys()
        if destination == "config":
            parser.add_argument("policy", type=str)
            parser.add_argument("capacity", type=int)
            parser.add_argument("clear_cache", type=bool)
            args = parser.parse_args()
            return set_config(args)
        return False, 400, None
