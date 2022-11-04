import werkzeug.datastructures
from flask_restful import Resource, reqparse, request
from .message import response
from .routes.key import create_key, get_key, list_keys

PARASER = reqparse.RequestParser()

class Api(Resource):

    def __init__(self):
        self.key = None

    @response
    def get(self):
        pass

    @response
    def post(self, key=None):
        urls = [
            "/api/upload",
            "/api/list_keys",
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
        return False, 400, None
