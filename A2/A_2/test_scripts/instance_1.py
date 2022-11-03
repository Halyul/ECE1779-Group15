import pathlib
import yaml

CONFIG = yaml.safe_load(open(pathlib.Path(__file__).parent.absolute().joinpath("..", "config.yaml"), "r"))

def get_config():
    pass

def get_status():
    pass

def upload():
    pass

def list_keys():
    pass

def set_config():
    pass

def get_key_image():
    pass

if __name__ == "__main__":
    print(get_config())
    print(get_status())
    print(upload())
    print(list_keys())
    print(set_config())
    print(get_key_image())