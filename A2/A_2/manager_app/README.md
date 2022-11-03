# Flask Instance 4 - manager_app

## Endpoints

URL                    		     | Method | Content Type     | Body                                               | Note
---------------------------------|--------|------------------|----------------------------------------------------|-----------------------------
/api/manager/node_num            | GET    | N/A              | N/A                                                | 
/api/manager/aggregate_stats     | GET    | N/A              | N/A                                                | 
/api/manager/poolsize/increase   | POST   | N/A              | N/A  |
/api/manager/poolsize/decrease   | POST   | N/A              | N/A                                                | 
/api/manager/poolsize/automatic  | POST   | application/json | `max_miss_rate_threshold`, `min_miss_rate_threshold`, `expand_ratio`, `shrink_ratio` | 
/api/manager/cache/clear         | DELETE | N/A              | N/A                                   |
/api/manager/data/clear          | DELETE | N/A              | N/A                                   |
                   

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
- [ ] Call function applying to multiple EC2 instances
