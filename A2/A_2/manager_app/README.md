# Flask Instance 4 - manager_app

## Endpoints

URL                    		       | Method | Content Type    | Body  | Note
---------------------------------|--------|-----------------|-------|-----------------------------
/api/manager/pool_node_list      | GET    | N/A             | N/A   |Return pool node list
/api/manager/poolsize/config     | GET    | N/A             | N/A   |Retrun pool resize option (auto/manual), and parameters(empty for manual)
/api/manager/poolsize            | GET    | N/A             | N/A   |Return pool size   
/api/manager/aggregate_stats     | GET    | N/A             | N/A   |Return 30 min data 
/api/manager/poolsize/manual     | POST   | application/json| `change` (accepted value:  `increase`,  `decrease`)|Notify instance 1 pool size will chagne. If `change` is `increase`, increase the pool size before notifying. Because the new node needs to be counted when moving key-image between partitions.
/api/poolsize/change             | POST   | N/A             | N/A   | Actually increase/decrease node
/api/manager/poolsize/automatic  | POST   | application/json| `max_miss_rate_threshold`, `min_miss_rate_threshold`, `expand_ratio`, `shrink_ratio` |Pass automatic paramters to auto_scalar 
/api/manager/config              | POST   | application/json| `capacity`, `replacement_policy`| Pass cache paramters to all memcache
/api/manager/cache/clear         | DELETE | N/A             | N/A   | Clear all cache data
/api/manager/data/clear          | DELETE | N/A             | N/A   | Clear all cache data, S3 and RDS
                   

## TODO

- [x] Get the number of nodes
- [x] Manual increase/decrease pool size 
- [x] Set auto-scalar parameters
- [x] Set memcache configuration
- [x] Clear all cache
- [ ] Clear all data
  - [x] EC2
  - [x] S3
  - [ ] RDS
- [ ] Get 30 mins aggregate statistics and chart
- [x] Call function applying to multiple EC2 instances
- [x] Notify instance 1 before destroying EC2 instance
- [ ] Create a task queue for concurrency manual resizing requests 
