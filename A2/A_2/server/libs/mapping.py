import hashlib

def get_str_md5(string):
    m = hashlib.md5()
    m.update(string.encode("utf-8"))
    return m

def find_partition(key):
    md5 = get_str_md5(key)
    partition = int.from_bytes(md5.digest(), byteorder="big") >> (4 * 31)
    return partition

def find_cached_node(cur_node_num, partition):
    return partition % cur_node_num

def rebalance(mode):
    
    pass