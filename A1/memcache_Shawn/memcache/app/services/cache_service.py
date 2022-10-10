import json
import math

from flask import request, jsonify

from memcache_Shawn.memcache.app import webapp, config
from memcache_Shawn.memcache.app.db_operations.configurations import get_capacity_in_mb_db, get_replacement_policy_db
from memcache_Shawn.memcache.app.services.helper import release_cache_memory


def get_cache():
    key = request.form.get('key')
    if key is None:
        response = webapp.response_class(
            response=json.dumps("Key cannot be empty"),
            status=400,
            mimetype='application/json'
        )
        return response

    config.memcache_request_nums += 1

    if key in config.memcache:
        config.memcache_total_hit += 1
        config.memcache_keys_ordered.remove(key)
        config.memcache_keys_ordered.append(key)
        value = config.memcache[key]
        response = webapp.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )
    return response


def create_cache():
    key = request.form.get('key')
    value = request.form.get('value')
    memory = int(config.memcache_config_capacity_in_mb)

    # Base 64 conversion, result in MB
    value = value.split("base64,")[1]
    size = math.ceil(len(value) / 4) * 3
    size /= (1024 * 1024)

    if key is None or value is None:
        response = webapp.response_class(
            response=json.dumps("Key or value cannot be empty"),
            status=400,
            mimetype='application/json'
        )
        return response

    if size > memory:
        response = webapp.response_class(
            response=json.dumps("The file size is larger than the cache memory"),
            status=400,
            mimetype='application/json'
        )
        return response

    while config.memcache_used_memory + size > memory:
        release_cache_memory()

    config.memcache[key] = value
    config.memcache_used_memory += size
    config.memcache_keys_ordered.append(key)

    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )
    return response


def delete_specific_cache():
    key = request.form.get('key')
    if key in config.memcache:
        image_size = len(config.memcache.pop(key))
        config.memcache_used_memory -= image_size
        config.memcache_keys_ordered.remove(key)
    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )
    return response


def delete_all_cache():
    config.memcache_used_memory = 0
    config.memcache.clear()
    config.memcache_keys_ordered.clear()
    response = webapp.response_class(
        response=json.dumps("No Content"),
        status=204,
        mimetype='application/json'
    )
    return response


def update_cache_configs():
    config.memcache_config_capacity_in_mb = get_capacity_in_mb_db()
    config.memcache_config_replacement_policy = get_replacement_policy_db()
    return jsonify(
        capacity_in_mb=config.memcache_config_capacity_in_mb,
        replacement_policy=config.memcache_config_replacement_policy,
    )