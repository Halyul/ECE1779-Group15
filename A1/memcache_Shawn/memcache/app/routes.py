from app import webapp
from app.services import cache_service


@webapp.route('/api/key/<key_value>', methods=['GET'])
def get(key_value):
    return cache_service.get_cache(key_value)


@webapp.route('/api/upload', methods=['POST'])
def put():
    return cache_service.create_cache()


@webapp.route('/api/key', methods=['DELETE'])
def clear():
    return cache_service.delete_all_cache()


@webapp.route('/api/config', methods=['GET'])
def refresh_configuration():
    return cache_service.get_cache_configuration()
