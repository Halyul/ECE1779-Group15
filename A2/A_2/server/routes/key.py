import mimetypes
import pathlib, base64, time
from server.config import Config
from server.libs.database import Database
from server.libs.thread_task import ThreadTask
import requests

CONFIG = Config().fetch()
CACHE_URL = "http://{host}:{port}".format(**CONFIG["cache"])
KEY_IMAGE_TABLE_NAME = CONFIG["database"]["table_names"]["key_image"]

def create_key(args):
    """
        1. Check if key name is valid
        2. Store file
        3. invalidate cache
        4. add/update entry to database
    """
    if " " in args["key"] or "" == args["key"] or len(args["key"]) > 48:
        return False, 400, "Key does not meet the requirement."
    file = args["file"]
    if file.content_type is None:
        return False, 400, "The upload request is invalid due to empty content type."
    if not file.content_type.startswith("image/"):
        return False, 403, "Only image file is allowed."
    database = Database()
    database.lock(table=KEY_IMAGE_TABLE_NAME)
    file_entry = database.get_key_image_pair(args["key"])
    if not file_entry:
        filepath = pathlib.Path.cwd().joinpath(CONFIG["server"]["upload_location"])
        filepath.mkdir(parents=True, exist_ok=True)
        file_ext = file.filename.split(".")[-1]
        filename = "{}.{}".format(str(int(time.time() * 1000)), file_ext)
        file_fullpath = filepath.joinpath(filename)
        database.create_key_image_pair(args["key"], filename)
    else:
        file_fullpath = pathlib.Path.cwd().joinpath(CONFIG["server"]["upload_location"], file_entry[0])
        # invalidate the key in the memcache
        ThreadTask(
            requests.delete, 
            kwargs=dict(
                url=CACHE_URL + "/api/cache/key", 
                data=[("key", args["key"])]
            )
        ).start()
    file.save(file_fullpath)
    database.unlock()
    return True, 200, None

def get_key(key):
    """
        1. ask cache if key-image exists
        2. If key exists, get the image from cache response
        3. If cache does not exist, get the key-image pair from database
        4. If key-image pair exists, get the image from local storage, convert to base64 and response to both webpage and cache
        5. If key-image pair does not exist, return 404 
    """
    if " " in key or "" == key or len(key) > 48:
        return False, 400, "Key does not meet the requirement."
    try:
        response = requests.post(CACHE_URL + "/api/cache/key", data=[("key", key)]).json()
        content = response["content"]
        return True, 200, dict(
            content=content
        )
    except Exception as e:
        database = Database()
        database.lock(table=KEY_IMAGE_TABLE_NAME)
        key_image_pair = database.get_key_image_pair(key)
        if key_image_pair is None:
            database.unlock()
            return False, 404, "No such key."
        content = None
        filepath = pathlib.Path.cwd().joinpath(CONFIG["server"]["upload_location"], key_image_pair[0])
        with open(filepath, "rb") as f:
            image_content = f.read()
            encoded_bytes = base64.b64encode(image_content)
            humanreadable_data = encoded_bytes.decode("utf-8")
            content = "data:{};base64,".format(mimetypes.guess_type(filepath)[0]) + humanreadable_data
        ThreadTask(
            requests.post,
            kwargs=dict(
                url = CACHE_URL + "/api/cache/content", 
                data = [('key', key), ('value', content)]
            )
        ).start()
        database.unlock()
        return True, 200, dict(
            content=content
        )

def list_keys():
    """
        1. List all keys in the database
    """
    database = Database()
    database.lock(table=KEY_IMAGE_TABLE_NAME)
    keys_entries = database.get_keys()
    database.unlock()
    return True, 200, dict(
        keys=[e[0] for e in keys_entries]
    )
