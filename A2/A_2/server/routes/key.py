import base64, time
from server.config import Config
from server.libs.database import Database
from server.libs.thread_task import ThreadTask
from server.aws.s3 import Bucket
from server.routes.pool import MAPPING, CACHED_KEYS
from server.libs.mapping import find_partition
import requests, logging

CONFIG = Config().fetch()
KEY_IMAGE_TABLE_NAME = CONFIG["database"]["table_names"]["key_image"]
BUCKET = Bucket(CONFIG["server"]["bucket"]["name"])

def create_key(args):
    """
        1. Check if key name is valid
        2. Store file
        3. invalidate cache
        4. add/update entry to database
    """
    key = args["key"]
    if " " in key or "" == key or len(key) > 48:
        return False, 400, "Key does not meet the requirement."
    file = args["file"]
    database = Database()
    database.lock(table=KEY_IMAGE_TABLE_NAME)
    file_entry = database.get_key_image_pair(key)
    logging.info("File entry: {}".format(file_entry))
    if not file_entry:
        filename = "{}.{}".format(str(int(time.time() * 1000)), "s3")
        logging.info("Created key-image pair: {}-{}".format(key, filename))
        database.create_key_image_pair(key, filename)
    else:
        filename = file_entry[0]
        logging.info("Updating key-image pair: {}-{}".format(key, filename))
        # invalidate the key in the memcache
        url = MAPPING.find_cached_node(find_partition(key)) + ":" + str(CONFIG["cache"]["port"]) + "/api/cache/key"
        logging.info("Invalidate cache request send to: {}".format(url))
        # ThreadTask(
        #     requests.delete, 
        #     kwargs=dict(
        #         url=url, 
        #         data=[("key", key)]
        #     )
        # ).start()
    file_base64 = "data:{};base64,".format(file.mimetype).encode("utf-8") + base64.b64encode(file.read())
    flag, resp = BUCKET.object.upload(file_base64, filename)
    if not flag:
        database.unlock()
        return False, 500, "Failed to upload the image."
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
        url = MAPPING.find_cached_node(find_partition(key)) + ":" + str(CONFIG["cache"]["port"]) + "/api/cache/key"
        response = requests.post(url, data=[("key", key)]).json()
        content = response["content"]
        return True, 200, dict(
            content=content
        )
    except Exception as e:
        database = Database()
        database.lock(table=KEY_IMAGE_TABLE_NAME)
        key_image_pair = database.get_key_image_pair(key)
        logging.info("Key image pair: {}".format(key_image_pair))
        if key_image_pair is None:
            database.unlock()
            return False, 404, "No such key."
        image_key = key_image_pair[0]
        flag, content = BUCKET.object.get(image_key)
        if not flag:
            database.unlock()
            return False, 500, "Failed to retrieve the image."
        url = MAPPING.find_cached_node(find_partition(key)) + ":" + str(CONFIG["cache"]["port"]) + "/api/cache/content"
        logging.info("Add cache request send to: {}".format(url))
        ThreadTask(
            requests.post,
            kwargs=dict(
                url = url, 
                data = [('key', key), ('value', content)]
            )
        ).start()
        CACHED_KEYS.add(key)
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

def clear(mode):
    if mode == "data":
        database = Database()
        database.lock(table=KEY_IMAGE_TABLE_NAME)
        database.clear_keys()
        database.unlock()
        BUCKET.object.delete_all()
        logging.info("Data Cleared.")
    CACHED_KEYS.remove_all()
    logging.info("Cache Cleared.")
    return True, 200, None
