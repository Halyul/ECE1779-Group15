# Flask Instance 1

## Endpoints

URL               | Method  | Content Type        | Body      
------------------|---------|---------------------|-------------
/api/upload       | POST    | multipart/form-data | `file`, `key` 
/api/list_keys    | POST    | application/json    | N/A
/api/key/<key>    | POST    | application/json    | N/A
/api/notify       | POST    | application/json    | `ip`

## TODO
- [x] Remove functionality to configure memcache settings.
- [x] Remove functionality that displays memcache statistics.
- [x] All image files should be stored in S3.
- [ ] The mapping between keys and image files should be stored in AWS RDS. Do not store the images themselves in the RDS database.
- [ ] Route requests to the memcache pool using a consistent hashing approach based on MD5 hashes. For simplicity, assume that the key space is partitioned into 16 equal-size regions which are then allocated to the pool of memcache nodes. Figures 1-3 illustrate how this assignment changes as the pool size changes from one node to two nodes to three nodes More information changes as the pool size changes from one node to two nodes, to three nodes. More information is provided in the Consistent Hashing section below.
  - [x] find_location(cur_node_num, find_partition(key))
  - [ ] Moving keys and values before cache access if pool size changed, "The assignment of key values to nodes changes each time a new node is added or removed, so ensure that you are updating nodes each time". (added by Teng Shu)
    - you move images whenever memcache nodes are added or removed, according to the new assignment of images to nodes (following the hashing shown in the assignment).
    - balance?
    - new api in manager to lock inc/desc until re-balance is done?
- [ ] Add a feature to the front-end that allows the front-end to be automatically notified when the size of the memcache pool changes. In response, the front-end should rebalance the mapping of key regions to nodes, and use the new allocation to route requests to the memcache
  - [x] new endpoint
  - [ ] balance
