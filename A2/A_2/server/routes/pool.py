import requests
import logging
from server.routes.key import CACHED_KEYS
from server.libs.mapping import Mapping
from server.libs.thread_task import ThreadTask
from server.config import Config

CONFIG = Config().fetch()
MAPPING = Mapping(CACHED_KEYS)

def pool_change(args):
    """
        receive: {
            node_ip: [<IPs>],
            mode: "manual" | "automatic",
            change: "increase" | "decrease"
        }
        send: {
            manager: "" | "<IP:Port of manager or autoscaler when to delete>"
            destination: {
                <Node A IP>: [<Keys>],
                <Node B IP>: [<Keys>]
            }
        }
    """
    ips = args["node_ip"]
    mode = args["mode"]
    change = args["change"]
    result = MAPPING.notify_change(ips, mode, change)
    for entry in result:
        url = entry["send_to"] + ":" + str(CONFIG["cache"]["port"])  + "/api/cache/move_keys"
        logging.info("Send to: {} with Paylod {}".format(url, entry["payload"]))
        # ThreadTask(
        #     requests.post, 
        #     kwargs=dict(
        #         url=entry["send_to"] + ":" + CONFIG["cache"]["port"]  + "/api/cache/move_keys", 
        #         data=entry["payload"]
        #     )
        # ).start()
    return True, 200, None