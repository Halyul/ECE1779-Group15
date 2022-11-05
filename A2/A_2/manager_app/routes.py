import services
from manager_app import webapp


@webapp.route('/api/manager/poolsize', methods=['GET'])
def get_pool_size():
    return services.get_pool_size()


@webapp.route('/api/manager/poolsize/config', methods=['GET'])
def get_resize_pool_config():
    return services.get_resize_pool_config()


@webapp.route('/api/manager/poolsize/manual', methods=['POST'])
def change_pool_size_manual():
    return services.change_pool_size_manual()


@webapp.route('/api/manager/poolsize/automatic', methods=['POST'])
def change_pool_size_auto():
    return services.set_auto_scaler_parameters()


@webapp.route('/api/manager/aggregate_stats', methods=['GET'])
def get_aggregate_stats():
    return


@webapp.route('/api/manager/cache/config', methods=['POST'])
def set_cache_configurations():
    return services.set_cache_configurations()


@webapp.route('/api/manager/cache/clear', methods=['DELETE'])
def clear_cache():
    return services.clear_all_cache()


@webapp.route('/api/manager/data/clear', methods=['DELETE'])
def clear_data():
    return services.clear_all_data()
