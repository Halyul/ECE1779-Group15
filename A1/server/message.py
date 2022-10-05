from functools import wraps

MESSAGES = {
    "200": "HTTP 200 OK",
    "400": "HTTP Bad Request",
    "401": "HTTP Unauthorized",
    "403": "Forbidden",
    "404": "HTTP Not Found",
    "500": "Internal Server Error"
}

def errorhandler(status_code, error=None):
    """
        Response proper error formate
        Args:
            self: access global variables
            status_code: status code
        Returns:
            str: error message
    """
    result = {
        "success": "false",
        "error": {
            "code": status_code,
            "message": error if error is not None else MESSAGES[str(status_code)],
        },
    }

    return result

def response(func):
    """
        Changes the message to fit the structure
            Args:
                self: access global variables
            func: decoration call
        Returns:
            json: message to response
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            status, code, message = func(*args, **kwargs)
            if status == True:
                result = {
                    "success": "true"
                }
            else:
                return errorhandler(code, message), code
            if message is not None:
                for k,v in message.items():
                    result[k] = v
            return result, code
        except Exception as e:
            print(e)
            return errorhandler(500, "Internal Server Error. Please Check Server Console."), 500
    return wrapper