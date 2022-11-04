import pathlib
import yaml
import requests
import json

CONFIG = yaml.safe_load(open(pathlib.Path(__file__).parent.absolute().joinpath("..", "config.yaml"), "r"))
BASE_URL = "http://localhost:" + str(CONFIG["server"]["port"])


def upload():
    # files = {
    #     "file": ("test.svg", open(pathlib.Path(__file__).parent.absolute().joinpath("src", "test.svg"), "rb"), "image/svg+xml")
    # }
    files = {
        "file": open(pathlib.Path(__file__).parent.absolute().joinpath("src", "test.svg"), "rb")
    }
    data = {
        "key": "123"
    }
    # print(requests.Request('POST', BASE_URL + "/api/upload", files=files, data=data).prepare().body.decode('utf8'))
    r = requests.post(BASE_URL + "/api/upload", files=files, data=data)
    return r.json()

def list_keys():
    r = requests.post(BASE_URL + "/api/list_keys")
    return r.json()

def get_key_image():
    r = requests.post(BASE_URL + "/api/key/123")
    return r.json()

if __name__ == "__main__":
    print(upload())
    print(list_keys())
    print(get_key_image())