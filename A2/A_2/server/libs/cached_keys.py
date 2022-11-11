import logging
from server.libs.mapping import find_partition

class CachedKeys:
    def __init__(self):
        self.keys = dict()
    
    def add(self, key):
        self.keys[key] = find_partition(key)
        logging.info("Key: {}, Partition: {}".format(key, self.keys[key]))
    
    def remove_all(self):
        self.keys = dict()
        logging.info("Cached keys cleared")
    
    def list(self):
        return self.keys