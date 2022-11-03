import json
from manager_app import webapp


def failed_response(code, message):
    json_response = {
        "success": "false",
        "error": {
            "code": code,
            "message": message
        }
    }
    response = webapp.response_class(
        response=json.dumps(json_response),
        status=400,
        mimetype='application/json'
    )
    return response


def success_response(content):
    json_response = {
        "success": "true",
        "content": content
    }
    response = webapp.response_class(
        response=json.dumps(json_response),
        status=200,
        mimetype='application/json'
    )
    return response
