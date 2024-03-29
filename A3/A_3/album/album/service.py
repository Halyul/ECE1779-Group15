import base64, time
import math
from datetime import datetime
import mimetypes
from decimal import Decimal

import werkzeug
from flask import request
from flask_restful import reqparse

from album.aws.dynamoDB_admin import db_get_image_by_key_admin, db_get_all_images_admin
from album.aws.dynamoDB_common import db_upload_image, db_update_access_time, db_delete_image, \
    db_set_is_shared, CAPACITY, db_get_stats_from_table, IMAGE_NUMBER, USER_NUMBER, CALL_NUMBER, update_statistics, \
    db_get_table_stats, db_reset_share
from album.aws.dynamoDB_user import db_is_allowed_get_shared_image, db_get_all_images_user, db_get_image_by_key_user

from album.aws.s3 import Bucket
import logging

BUCKET = Bucket("ece1779a3hx")
ADMIN = "admin"


def upload_image():
    update_statistics(CALL_NUMBER, 1)

    data = request.form.to_dict()
    key = data["key"]
    if " " in key or "" == key or len(key) > 48:
        return False, 400, "Key does not meet the requirement."
    file = request.files["file"]
    file_content = file.read()
    extension = file.filename.rsplit('.', 1)[1].lower()

    size = len(file_content) / (1024 * 1024)
    update_statistics(CAPACITY, Decimal(size))

    user = data["user"]
    role = data["role"]

    filename = "{}.{}".format(str(int(time.time() * 1000)), extension)
    time_stamp = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    image_meta = db_get_image_by_key_admin(key)
    if image_meta:
        if image_meta.get('user') != user:
            return False, 500, "Failed to upload the image. Key must be unique."
    else:
        db_upload_image(key, filename, user, time_stamp)

    # file_base64 = file
    # file_base64 = "data:{};base64,".format(file.mimetype).encode("utf-8") + base64.b64encode(file.read())
    flag, resp = BUCKET.object.upload(file_content, filename)
    if not flag:
        return False, 500, "Failed to upload the image."
    return True, 200, None


def delete_image():
    """
    1. Get image meta from db based on key
    2. Reduce capacity
    3. Delete image from s3
    4. Delete s3 from s3
    5. Delete entry in database
    """
    update_statistics(CALL_NUMBER, 1)

    key = request.get_json()["key"]

    image_meta = db_get_image_by_key_admin(key)
    if image_meta:
        file_name = image_meta.get('image_name')
        thumbnail_name = image_meta.get('thumbnail')

        file = BUCKET.object.get(file_name)
        size = len(file[1]) / (1024 * 1024)
        # size = math.ceil(len(file.read())) / (1024 * 1024)
        update_statistics(CAPACITY, -1 * Decimal(size))

        BUCKET.object.delete(file_name)
        BUCKET.object.delete(thumbnail_name)
        logging.info("Key deleted")

        db_delete_image(key)
    else:
        return False, 400, "No such key"
    return True, 200, None


def share_image():
    update_statistics(CALL_NUMBER, 1)

    key = request.get_json()["key"]
    is_shared = request.get_json()["is_shared"]

    db_set_is_shared(key, is_shared)
    image_meta = db_get_image_by_key_admin(key)
    if db_is_allowed_get_shared_image(key) is False:
        db_reset_share(key)
        image_meta.update({"number_of_access": -1})
        image_meta.update({"share_link": None})

    file_name = image_meta.get('image_name')
    time_stamp = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    db_update_access_time(key, time_stamp)

    flag, thumbnail = BUCKET.object.get(image_meta.get('thumbnail'))
    thumbnail64 = "data:{};base64,".format(mimetypes.guess_type(image_meta.get('thumbnail'))[0]) + base64.b64encode(
        thumbnail).decode("utf-8")
    image_meta.update({"thumbnail": thumbnail64})

    flag, content = BUCKET.object.get(file_name)
    if not flag:
        return False, 500, "Failed to retrieve the image."

    content64 = "data:{};base64,".format(mimetypes.guess_type(file_name)[0]) + base64.b64encode(content).decode(
        "utf-8")
    image_meta['content'] = content64
    return True, 200, dict(
        image=image_meta
    )


def get_image_by_key():
    update_statistics(CALL_NUMBER, 1)

    key = request.get_json()["key"]
    user = request.get_json()["user"]
    role = request.get_json()["role"]

    if " " in key or "" == key or len(key) > 48:
        return False, 400, "Filter does not meet the requirement."

    # Get public image
    if role is None:
        image_meta = db_get_image_by_key_admin(key)
        if not db_is_allowed_get_shared_image(key):
            image_meta.update({"number_of_access": -1})
            image_meta.update({"share_link": None})
    else:
        if role == ADMIN:
            image_meta = db_get_image_by_key_admin(key)
        else:
            image_meta = db_get_image_by_key_user(user, key)

    if image_meta is None:
        return False, 404, "No such key."
    else:
        file_name = image_meta.get('image_name')
        time_stamp = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        db_update_access_time(key, time_stamp)

        flag, thumbnail = BUCKET.object.get(image_meta.get('thumbnail'))
        thumbnail64 = "data:{};base64,".format(mimetypes.guess_type(image_meta.get('thumbnail'))[0]) + base64.b64encode(thumbnail).decode("utf-8")
        image_meta.update({"thumbnail": thumbnail64})

        flag, content = BUCKET.object.get(file_name)
        if not flag:
            return False, 500, "Failed to retrieve the image."

        content64 = "data:{};base64,".format(mimetypes.guess_type(file_name)[0]) + base64.b64encode(content).decode("utf-8")
        image_meta['content'] = content64
        return True, 200, dict(
            image=[image_meta]
        )


def list_all_multi_attributes():
    update_statistics(CALL_NUMBER, 1)

    user = request.get_json()["user"]
    role = request.get_json()["role"]
    admin = request.get_json()["admin"]

    if admin:
        image_meta = db_get_all_images_admin()
    else:
        image_meta = db_get_all_images_user(user)

    for item in image_meta:
        flag, thumbnail = BUCKET.object.get(item.get('thumbnail'))
        thumbnail64 = "data:{};base64,".format(mimetypes.guess_type(item.get('thumbnail'))[0]) + base64.b64encode(thumbnail).decode("utf-8")
        item.update({"thumbnail": thumbnail64})

    return True, 200, dict(
        images=image_meta
    )


def get_stats():
    update_statistics(CALL_NUMBER, 1)
    stats = [
        dict(name="Capacity", value=db_get_stats_from_table(CAPACITY)),
        dict(name="Total Number of Images", value=db_get_table_stats().get('image_number')),
        dict(name="Total Number of Active Users", value=db_get_table_stats().get('user_number')),
        dict(name="Number of Lambda Function Calls", value=db_get_stats_from_table(CALL_NUMBER))
    ]
    return True, 200, dict(
        stats=stats
    )
