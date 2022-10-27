from memcache_Shawn.memcache.app import webapp
from memcache_Shawn.memcache.app.services import cache_service


@webapp.route('/api/cache/content', methods=['POST'])
def put():
    return cache_service.create_cache()


@webapp.route('/api/cache/key', methods=['POST'])
def get():
    return cache_service.get_cache()


@webapp.route('/api/cache', methods=['DELETE'])
def clear():
    return cache_service.delete_all_cache()


@webapp.route('/api/cache/key', methods=['DELETE'])
def invalidate_key():
    return cache_service.delete_specific_cache()


@webapp.route('/api/cache/config', methods=['GET'])
def refresh_configuration():
    return cache_service.update_cache_configs()
