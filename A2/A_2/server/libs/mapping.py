import hashlib
import requests
import logging
from server.config import Config

CONFIG = Config().fetch()
MANAGER_URL = "http://{host}:{port}".format(**CONFIG["manager"])
logging.basicConfig(level=logging.INFO)

def get_str_md5(string):
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m

def find_partition(key):
    md5 = get_str_md5(key)
    partition = int.from_bytes(md5.digest(), byteorder="big") >> (4 * 31)
    return partition

class Mapping:
    def __init__(self, CACHED_KEYS):
        self.size = CONFIG["cache"]["partitions"]
        self.nodes = self.get_current_nodes()
        self.mapping = self.generate_mapping()
        self.CACHED_KEYS = CACHED_KEYS
        logging.info("Current nodes: {}".format(self.nodes))
        logging.info("Mapping: {}".format(self.mapping))

    def get_current_nodes(self):
        response = requests.get(MANAGER_URL + "/api/manager/pool_node_list")
        if response.status_code != 200:
            logging.error("Error when getting current nodes: {}".format(response.text))
            raise

        resp = response.json()["content"]["node_ip_list"]

        logging.info("Current nodes: {}".format(resp))
        return resp
    
    def generate_mapping(self):
        output = dict()
        node_index = lambda x: x % len(self.nodes)
        j = 0
        for i in range(self.size):
            output[i] = self.nodes[node_index(j)]
            j += 1
        return output
    
    # PATH: server/routes/key.py
    def find_cache_location(self, partition):
        result = self.mapping[partition % len(self.nodes)]
        logging.info("Cache location: {}".format(result))
        return result

    def notify_change(self, nodes, mode, change):
        for node in nodes:
            if change == "increase":
                self.nodes.append(node)
            else:
                if node in self.nodes:
                    self.nodes.remove(node)
        difference = self.compute_difference()
        balance_result = self.balance(difference, nodes, mode)
        return balance_result

    def compute_difference(self):
        old_mapping = self.mapping
        self.mapping = self.generate_mapping()
        logging.info("Old mapping: {}".format(old_mapping))
        logging.info("New mapping: {}".format(self.mapping))
        old_new_mapping = {}
        for key in old_mapping.keys():
            if old_mapping[key] != self.mapping[key]:
                if old_mapping[key] not in old_new_mapping:
                    old_new_mapping[old_mapping[key]] = list()
                old_new_mapping[old_mapping[key]].append((key, self.mapping[key]))
        logging.info("Old-new mapping: {}".format(old_new_mapping))
        return old_new_mapping
    
    def balance(self, difference, nodes_to_delete, mode):
        output = []
        port = CONFIG["manager"]["port"] if mode == "manual" else CONFIG["auto_scaler"]["port"]
        current_cached_key_list = self.CACHED_KEYS.list()
        logging.info("Current cached keys: {}".format(current_cached_key_list))
        for key, value in difference.items():
            result = dict(
                send_to=key,
                payload=dict(
                    port=port if key in nodes_to_delete else -1,
                    dest=dict()
                )
            )
            for item in value:
                if item[0] in current_cached_key_list:
                    if item[1] not in result["payload"]["dest"]:
                        result["payload"]["dest"][item[1]] = list()
                    for i in current_cached_key_list[item[0]]:
                        result["payload"]["dest"][item[1]].append(i)
            if len(result["payload"]["dest"]) != 0 or key in nodes_to_delete:
                output.append(result)
        logging.info("Balance result: {}".format(output))
        return output
    
    def find_cached_node(self, partition):
        index = partition % len(self.nodes)
        return self.nodes[index]

    def get_nodes(self):
        return self.nodes