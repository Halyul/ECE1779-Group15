import server.config

add_one_min_data_thread_stop = False

# Config from config.yaml
config_info = server.config.Config().fetch()
cache_port = config_info['cache']['port']
server_port = config_info['server']['port']
auto_scaler_port = config_info['auto_scaler']['port']
manager_port = config_info['manager']['port']
AUTO_SCALAR_URL = "http://127.0.0.1:" + str(auto_scaler_port)
SERVER_URL = "http://127.0.0.1:" + str(server_port)
STATIC_FOLDER = config_info["manager"]["static_folder"]

# aws configs
ami_id = config_info['aws']['ami_id']
subnet_id = config_info['aws']['subnet_id']
security_group_id = config_info['aws']['security_group_id']
ssh_key_name = config_info['aws']['ssh_key_name']
private_key_file = config_info['aws']['private_key_file']
credential_file = config_info['aws']['credential_file']

# github
github_access_token = config_info['github']['access_token']