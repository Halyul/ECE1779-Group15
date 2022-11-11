import os
from flask import send_from_directory
import services
from manager_app import webapp


@webapp.route("/", defaults={"path": ""})
@webapp.route("/<path:path>")
def serve(path):
    def set_mimetype(filename: str):
        if filename.endswith("js"):
            return "text/javascript"
        elif filename.endswith("css"):
            return "text/css"
        elif filename.endswith("svg"):
            return "image/svg+xml"

    if path != "" and os.path.exists(webapp.static_folder + "/" + path):
        return send_from_directory(
            webapp.static_folder, 
            path,
            mimetype=set_mimetype(path)
        )
    else:
        return send_from_directory(webapp.static_folder, "index.html")

@webapp.route('/api/manager/pool_node_list', methods=['GET'])
def get_pool_size():
    return services.get_pool_node_list()


@webapp.route('/api/manager/poolsize/config', methods=['GET'])
def get_resize_pool_config():
    return services.get_resize_pool_config()


@webapp.route('/api/manager/aggregate_stats', methods=['GET'])
def get_aggregate_stats():
    return


@webapp.route('/api/manager/poolsize', methods=['GET'])
def get_pool_size():
    return services.get_pool_size()


@webapp.route('/api/manager/cache/config', methods=['GET'])
def set_cache_configurations():
    return services.get_cache_configurations()


@webapp.route('/api/manager/poolsize/manual', methods=['POST'])
def notify_pool_size_change():
    return services.notify_pool_size_change()


@webapp.route('/api/poolsize/change', methods=['POST'])
def change_pool_size_manual():
    return services.change_pool_size_manual()


@webapp.route('/api/manager/poolsize/automatic', methods=['POST'])
def change_pool_size_auto():
    return services.set_auto_scaler_parameters()


@webapp.route('/api/manager/cache/config', methods=['POST'])
def set_cache_configurations():
    return services.set_cache_configurations()


@webapp.route('/api/manager/cache/clear', methods=['DELETE'])
def clear_cache():
    return services.clear_all_cache()


@webapp.route('/api/manager/data/clear', methods=['DELETE'])
def clear_data():
    return services.clear_all_data()
