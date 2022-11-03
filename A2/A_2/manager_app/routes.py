import ec2_helper_functions
import services
from manager_app import webapp


@webapp.route('/api/manager/node_num', methods=['GET'])
def get_node_num():
    return services.get_node_num()


@webapp.route('/api/manager/aggregate_stats', methods=['GET'])
def get_aggregate_stats():
    return


@webapp.route('/api/manager/poolsize/increase', methods=['POST'])
def increase_pool_size():
    return services.increase_pool_size()


@webapp.route('/api/manager/poolsize/decrease', methods=['DELETE'])
def decrease_pool_size():
    return services.decrease_pool_size()


@webapp.route('/api/manager/poolsize/automatic', methods=['POST'])
def decrease_pool_size():
    return services.set_auto_scaler_parameters()


@webapp.route('/api/manager/cache/clear', methods=['DELETE'])
def clear_cache():
    return services.clear_all_cache()


@webapp.route('/api/manager/data/clear', methods=['DELETE'])
def clear_data():
    return services.clear_all_data()
