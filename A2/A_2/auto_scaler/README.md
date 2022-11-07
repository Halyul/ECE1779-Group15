# Flask Instance 3 - auto scaler

## Endpoints

URL                      |  Method  | Content Type        | Body                                               | Note
-------------------------|----------|---------------------|----------------------------------------------------|-----------------------------
/                        | GET      | N/A                 | N/A                                                | for testing only: home page
/api/scaler/             | GET      | N/A                 | N/A                                                | for testing only: home page
/api/scaler/config       | POST     | application/json    | `max_miss_rate_threshold`, `min_miss_rate_threshold`, `expand_ratio`, `shrink_ratio`, `auto_mode` | set the auto scaler config
/api/scaler/terminate_all| POST     | N/A                 | N/A                                                | for testing only: terminate all nodes
/api/scaler/list         | GET/POST | N/A                 | N/A                                                | for testing only: a page listing all ec2 instancces
/api/scaler/set_test_miss_rate | POST | N/A               | `test_miss_rate`                                   | for testing only: send a test_miss_rate and then force a pool size adjustment
/api/scaler/cache_list   | GET      | N/A                 | N/A                                                | to get the current list of nodes' ids
/api/scaler/cache_list   | POST     | application/json    | `cache_pool_ids`                                   | to change the current list of nodes' ids
/api/poolsize/change     | POST     | application/json    | `cache_ip`                                         | to actually do the node deletion
                             

## TODO
- [x] There should be no need to manually restart the auto-scaler every time the policy is changed.
	- once policy/config changed, manager-app should send a http request to '/api/scaler/config' to update auto scaler
- [x] It should monitor the miss rate of the mecache pool by getting this information using the AWS CloudWatch API
- [ ] Check for the cache miss rate every one minute, then resizes the memcache pool
	- [x] total_GET_request_served will be get from node 0 (assume cache GET will send to all cache nodes as no way to know which cache may have the key after pool size change)
	- [x] total_hit will be calculated by summing all num_hit from cache nodes (not sure yet how to handle pool size change, maybe clear all cache statistics once pool size changed?)
- [x] Do NOT use the AWS Auto Scaling feature for this assignment.
- [x] Limit the maximum size of the memcache node pool set by auto-scaler to 8 and the minimum to 1. 
- [x] cache nodes need to be brought up by code
- [x] cache nodes need to be destroyed by code
- [x] a new API to get cache id list from elsewhere
- [x] a new API to send cache id list
- [ ] tell A1 there are nodes to be removed
- [x] a new API to actually remove the node
