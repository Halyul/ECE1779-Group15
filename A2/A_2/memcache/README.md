# Flask Instance 2 - mem-cache

## Endpoints

URL                      |  Method  | Content Type        | Body                                               | Note
-------------------------|----------|---------------------|----------------------------------------------------|-----------------------------
/api/cache/key           | POST     | application/json    | `key`                                              | GET a value for a key
/api/cache/key           | DELETE   | application/json    | `key`                                              | invalidate a key
/api/cache/content       | POST     | application/json    | `key`, `value`                                     | PUT a key value pair
/api/cache/config        | POST     | application/json    | `capacity`, `replacement_policy`, `[cache_index]`  | set the mem-cache config
/api/cache 	             | DELETE   | application/json    | N/A                                                | clear the mem-cache content
/api/cache/statistics    | GET      | application/json    | N/A                                                | legacy code, returns statistics in json format
/api/cache/set_num_hit   | POST     | N/A                 | `num_hit`                                          | legacy code, should not be used
/                        | GET      | N/A                 | N/A                                                | for testing only: home page
/keys                    | GET/POST | application/json    | N/A                                                | for testing only: returns a list of keys in cache
/api/cache/statistics    | POST     | N/A                 | N/A                                                | for testing only: cache info page
/api/cache/move_keys     | POST     | N/A                 | `dict{manager, dest, cache_ip}`                    | for key moving while change pool size, and to do node remove
                             

## TODO
- [x] Store memcache statistic every 5 seconds using CloudWatch Custom Metrics instead of the database as was done in A1
- [x] Add 'cache_index' to config so as to separate the data send to CloudWatch Custom Metrics
- [x] Remove the use of SQL
- [ ] add an API to handle 1) moving key-value pair to other nodes 2) initiate the node delete if this is the node that needs to be deleted
  - dict['manager'] should be `ip:port` if this node needs to be deleted, or "" if this node is not
  - dict['dest'] should be a dict in format of `{node_ip : [keys]}`
  - dict['cache_ip'] should be the ipv4 address of this cache, this will eventually send to the manager and auto_scaler to remove a specific cache node
