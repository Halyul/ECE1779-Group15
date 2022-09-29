import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='react/dist')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    def set_mimetype(filename: str):
        if filename.endswith("js"):
            return "text/javascript"
        elif filename.endswith("css"):
            return "text/css"
        elif filename.endswith("svg"):
            return "image/svg+xml"

    if path != "" and os.path.exists(app.static_folder + '/' + path):
        print(path)
        return send_from_directory(
            app.static_folder, 
            path,
            mimetype=set_mimetype(path)
        )
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/config")
def summary():
    d = dict(
        success="true",
        config=dict(
            policy="rr",
            capacity=100
        )
    )
    return d

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)