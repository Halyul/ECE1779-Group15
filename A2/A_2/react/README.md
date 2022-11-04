# Frontend

## Requests

URL            |  Method | Content Type        | Body      
---------------|---------|---------------------|-------------
/api/upload    | POST    | multipart/form-data | `file`, `key` 
/api/list_keys | POST    | application/json    | N/A
/api/key/<key> | POST    | application/json    | N/A                               

## TODO
### Web Frontend part
- [x] Remove functionality to configure memcache settings.
- [x] Remove functionality that displays memcache statistics.
- [ ] Route requests to the memcache pool using a consistent hashing approach based on MD5 hashes. For simplicity, assume that the key space is partitioned into 16 equal-size regions which are then allocated to the pool of memcache nodes. Figures 1-3 illustrate how this assignment changes as the pool size changes from one node to two nodes to three nodes More information changes as the pool size changes from one node to two nodes, to three nodes. More information is provided in the Consistent Hashing section below.
- [ ] Add a feature to the front-end that allows the front-end to be automatically notified when the size of the memcache pool changes. In response, the front-end should rebalance the mapping of key regions to nodes, and use the new allocation to route requests to the memcache

### Manager APP UI
- [ ] Use charts to show the number of nodes as well as to aggregate statistics for the memcache pool including miss rate, hit rate, number of items in cache, total size of items in cache, number of requests served per minute. The charts should display data for the last 30 minutes at 1-minute granularity
- [ ] Configure the capacity and replacement policy used by memcache nodes. All memcache nodes in the pool will operate with the same configuration.
- [ ] Selecting between two mutually-exclusive options for resizing the memcache pool:
    - [ ] Manual mode. There should be two buttons for manually growing the pool size by one node and shrinking the pool size by one node The maximum and minimum sizes should be 1 and shrinking the pool size by one node. The maximum and minimum sizes should be 1 and 8, respectively.
    - [ ] Automatic. Configure a simple auto-scaling policy by setting the following parameters (more details on the auto-scaler in component 2 below):
        - [ ] Max Miss Rate threshold (average for all nodes in the pool over the past 1 minute) for growing the pool.
        - [ ] Min Miss Rate threshold (average for all nodes in the pool over the past 1 minute) for shrinking the pool.
        - [ ] Ratio by which to expand the pool (e.g., expand ratio of 2.0, doubles the number of memcache nodes).
        - [ ] Ratio by which to shrink the pool (e.g., shrink ratio of 0.5, shuts down 50% of the current memcache nodes).
- [ ] Deleting all application data: A button to delete image data stored in RDS as well as all image files stored in S3, and clear the content of all memcache nodes in the pool (see next section on clearing memachce data).
- [ ] Clearing memcache data: A button to clear the content of all memcache nodes in the pool
