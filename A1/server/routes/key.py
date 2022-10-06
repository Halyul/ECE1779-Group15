import mimetypes
import pathlib, base64, time
from server.config import Config
from server.libs.database import Database
DB = Database()
CONFIG = Config().fetch()

def create_key(args):
    """
        1. Check if key name is valid
        2. Store file
        3. invalidate cache
        4. add/update entry to database
    """
    if " " in args["key"]:
        return False, 400, dict(
            message="Key cannot contain spaces"
        )
    file = args["file"]
    if not file.content_type.startswith("image/"):
        return False, 400, "Only image file is allowed."
    file_entry = DB.get_key_image_pair(args["key"])
    if not file_entry:
        filepath = pathlib.Path.cwd().joinpath(CONFIG["server"]["upload_location"])
        filepath.mkdir(parents=True, exist_ok=True)
        file_ext = file.filename.split(".")[-1]
        filename = "{}.{}".format(str(int(time.time() * 1000)), file_ext)
        file_fullpath = filepath.joinpath(filename)
        DB.create_key_image_pair(args["key"], filename)
    else:
        file_fullpath = pathlib.Path.cwd().joinpath(CONFIG["server"]["upload_location"], file_entry[0])
        # TODO: invalidate cache
    file.save(file_fullpath)
    return True, 200, None

def get_key(key):
    """
        1. ask cache if key-image exists
        2. If key exists, get the image from cache response
        3. If cache does not exist, get the key-image pair from database
        4. If key-image pair exists, get the image from local storage, convert to base64 and response to both webpage and cache
        5. If key-image pair does not exist, return 404 
    """
    # TODO: 1 - 2
    key_image_pair = DB.get_key_image_pair(key)
    if not key_image_pair:
        return False, 404, "No such key."
    content = None
    filepath = pathlib.Path.cwd().joinpath(CONFIG["server"]["upload_location"], key_image_pair[0])
    with open(filepath, "rb") as f:
        image_content = f.read()
        encoded_bytes = base64.b64encode(image_content)
        humanreadable_data = encoded_bytes.decode("utf-8")
        content = "data:{};base64,".format(mimetypes.guess_type(filepath)[0]) + humanreadable_data
    return True, 200, dict(
        content=content
    )

def list_keys():
    """
        1. List all keys in the database
    """
    keys_entries = DB.get_keys()
    return True, 200, dict(
        keys=[e[0] for e in keys_entries]
    )
