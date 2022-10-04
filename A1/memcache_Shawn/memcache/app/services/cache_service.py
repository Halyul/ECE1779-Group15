import datetime
import json

from flask import request, jsonify

from app import webapp, config
from app.db_operations.configurations import get_capacity_in_mb_db, get_replacement_policy_db
from app.db_operations.keys import delete_all_keys_db, update_time_last_used_db
from app.services.helper import delete_specific_cache, release_cache_memory


def get_cache(key):
    config.request_nums += 1

    if key is None:
        response = webapp.response_class(
            response=json.dumps("Key cannot be empty"),
            status=400,
            mimetype='application/json'
        )
        return response

    if key in config.memcache:
        value = config.memcache[key]
        current_time = datetime.datetime.now()
        update_time_last_used_db(current_time, key)
        response = webapp.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
        config.miss_nums += 1
        response = webapp.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )
    return response


def create_cache():
    config.request_nums += 1

    key = request.form.get('key')
    value = request.form.get('value')
    size = int(request.form.get('image_size'))

    if key in config.memcache:
        delete_specific_cache(key)
    else:
        memory = int(get_capacity_in_mb_db())
        while config.memcache_used_memory + size > memory:
            release_cache_memory()

        config.memcache[key] = value
        config.memcache_used_memory += size

    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response


def delete_all_cache():
    config.request_nums += 1
    config.memcache_used_memory = 0
    config.memcache.clear()
    delete_all_keys_db()
    response = webapp.response_class(
        response=json.dumps("No Content"),
        status=204,
        mimetype='application/json'
    )
    return response


def get_cache_configuration():
    config.request_nums += 1
    capacity_in_mb = get_capacity_in_mb_db()
    replacement_policy = get_replacement_policy_db()
    return jsonify(
        capacity_in_mb=capacity_in_mb,
        replacement_policy=replacement_policy
    )


