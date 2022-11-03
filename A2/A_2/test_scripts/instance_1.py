import pathlib
import yaml
import requests
import json

CONFIG = yaml.safe_load(open(pathlib.Path(__file__).parent.absolute().joinpath("..", "config.yaml"), "r"))
BASE_URL = "http://localhost:" + str(CONFIG["server"]["port"])

def get_config():
    r = requests.get(BASE_URL + "/api/config")
    return r.json()

def get_status():
    r = requests.get(BASE_URL + "/api/status")
    return r.json()

def upload():
    payload = {
        "file": open(pathlib.Path(__file__).parent.absolute().joinpath("src", "test.svg"), "rb")
    }
    data = {
        "key": "123"
    }
    r = requests.post(BASE_URL + "/api/upload", files=payload, data=data)
    return r.json()

def list_keys():
    r = requests.post(BASE_URL + "/api/list_keys")
    return r.json()

def set_config():
    original = get_config()["config"]
    r = requests.post(BASE_URL + "/api/config", 
                    json=dict(
                        policy="lru",
                        capacity=200
                    )
                )
    output = r.json()
    r = requests.post(BASE_URL + "/api/config",
                    json=original
                )
    return output

def get_key_image():
    r = requests.post(BASE_URL + "/api/key/123")
    return r.json()

if __name__ == "__main__":
    print(get_config())
    print(get_status())
    print(upload())
    print(list_keys())
    print(set_config())
    print(get_key_image())