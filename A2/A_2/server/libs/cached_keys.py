import logging
from server.libs.mapping import find_partition

class CachedKeys:
    def __init__(self):
        self.keys = dict()
    
    def add(self, key):
        partition = find_partition(key)
        if partition not in self.keys:
            self.keys[partition] = set()
        self.keys[partition].add(key)
        logging.info("Added cached key: {}, Partition: {}".format(key, partition))
    
    def remove_all(self):
        self.keys = dict()
        logging.info("Cached keys cleared")
    
    def list(self):
        return self.keys
