import os, logging
from flask import Flask, jsonify, send_from_directory, make_response
from flask_restful import Api as RestfulApi
from flask_cors import CORS
from album.message import errorhandler
from album.config import Config
from album import webapp

#
# @webapp.errorhandler(400)
# def bad_request(error):
#     return make_response(jsonify(errorhandler(400)), 400)
#
#
# @webapp.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify(errorhandler(404)), 404)
#
#
# @webapp.errorhandler(500)
# def server_error(error):
#     return make_response(jsonify(errorhandler(500)), 500)


webapp.run('0.0.0.0', 5009, debug=False)
