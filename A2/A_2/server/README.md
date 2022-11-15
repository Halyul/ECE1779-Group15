# Flask Instance 1

## Endpoints

URL               | Method  | Content Type        | Body      
------------------|---------|---------------------|-------------
/api/upload       | POST    | multipart/form-data | `file`, `key` 
/api/list_keys    | POST    | application/json    | N/A
/api/key/{key}    | POST    | application/json    | N/A
/api/notify       | POST    | application/json    | `node_ip`, `mode`, `change`
/api/clear/{data, cache} | DELETE | N/A | N/A

## AWS Setup
### Preamble
- The Main EC2 Instance refers to the EC2 instance which hosts Instace 1, Manager, and Auto-Scaler.
- Make sure the Main EC2 Instance has the correct `config` and `credentials` under `.aws`. The Main EC2 Instance, S3, and RDS must be under the same AWS account.

### S3
1. Create a bucket [here](https://s3.console.aws.amazon.com/s3/bucket/create)
2. Make sure the `region` matches the region of the Main EC2 Instance
3. Bucket name is set under `config.yaml -> server -> bucket -> name` (currently set to `ece1779assignment2group15`)
4. Leave everything else as default settings.

### RDS
0. Start the Main EC2 Instance
1. Create a database [here](https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#launch-dbinstance:gdb=false;isHermesCreate=true;s3-import=false)
2. Select `Standard create` under `Choose a database creation method`
3. Select `MySQL` under `Engine options`
4. Select `Free tier` under `Templates`
5. Under `Settings`:
  1. `Master username` is set under `config.yaml -> database -> user` (currently set to `root`)
  2. `Master password` is set under `config.yaml -> database -> password` (currently set to `ece1779pass`)
6. Select `db.t2.micro` under `Instance configuration`
7. Under `Storage`:
  1. Set `Allocated storage` to `20`
  2. Set `Maximum storage threshold` to `22`
8. Under `Connectivity`
  1. Select `Connect to an EC2 compute resource` under `Compute resource`
  2. Select the Main EC2 Instance under `EC2 Instance`
9. Leave everything else as default settings.
10. Create the database
11. When creation finished, go to the detail page of the database, copy the `Endpoint` URL under `Connectivity & security`
12. `ssh` into the Main EC2 Instance
  1. Paste the URL to `config.yaml -> database -> host`
  2. Test the database connection by running `mysql -h <Endpoint URL> -P 3306 -u <database username> -p`, enter the database password. If MySQL spawns a shell, means the database is created successfully and can be connected normally.
  2. Run `python3 create_database.py`

## Balance Result
[A, B, C, D] -> [A, B, C]
```
INFO:root:Old mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'A', 9: 'B', 10: 'C', 11: 'D', 12: 'A', 13: 'B', 14: 'C', 15: 'D'}
INFO:root:New mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'A', 4: 'B', 5: 'C', 6: 'A', 7: 'B', 8: 'C', 9: 'A', 10: 'B', 11: 'C', 12: 'A', 13: 'B', 14: 'C', 15: 'A'}
INFO:root:Old-new mapping: {'D': [(3, 'A'), (7, 'B'), (11, 'C'), (15, 'A')], 'A': [(4, 'B'), (8, 'C')], 'B': [(5, 'C'), (9, 'A')], 'C': [(6, 'A'), (10, 'B')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'D', 'payload': {'port': 5004, 'dest': {'C': ['k1']}}}, {'send_to': 'C', 'payload': {'port': -1, 'dest': {'A': ['k2']}}}]
INFO:root:Send to: D:5001/api/cache/move_keys with Paylod {'port': 5004, 'dest': {'C': ['k1']}}
INFO:root:Send to: C:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'A': ['k2']}}
```
[A, B, C] -> [A, B, C, D]
```
INFO:root:Old mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'A', 4: 'B', 5: 'C', 6: 'A', 7: 'B', 8: 'C', 9: 'A', 10: 'B', 11: 'C', 12: 'A', 13: 'B', 14: 'C', 15: 'A'}
INFO:root:New mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'A', 9: 'B', 10: 'C', 11: 'D', 12: 'A', 13: 'B', 14: 'C', 15: 'D'}
INFO:root:Old-new mapping: {'A': [(3, 'D'), (6, 'C'), (9, 'B'), (15, 'D')], 'B': [(4, 'A'), (7, 'D'), (10, 'C')], 'C': [(5, 'B'), (8, 'A'), (11, 'D')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'A', 'payload': {'port': -1, 'dest': {'C': ['k2']}}}, {'send_to': 'C', 'payload': {'port': -1, 'dest': {'D': ['k1']}}}]
INFO:root:Send to: A:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'C': ['k2']}}
INFO:root:Send to: C:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'D': ['k1']}}
```
[A, B, C, D] -> [A, B]
```
INFO:root:Old mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'A', 9: 'B', 10: 'C', 11: 'D', 12: 'A', 13: 'B', 14: 'C', 15: 'D'}
INFO:root:New mapping: {0: 'A', 1: 'B', 2: 'A', 3: 'B', 4: 'A', 5: 'B', 6: 'A', 7: 'B', 8: 'A', 9: 'B', 10: 'A', 11: 'B', 12: 'A', 13: 'B', 14: 'A', 15: 'B'}
INFO:root:Old-new mapping: {'C': [(2, 'A'), (6, 'A'), (10, 'A'), (14, 'A')], 'D': [(3, 'B'), (7, 'B'), (11, 'B'), (15, 'B')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'C', 'payload': {'port': 5004, 'dest': {'A': ['k2']}}}, {'send_to': 'D', 'payload': {'port': 5004, 'dest': {'B': ['k1']}}}]
INFO:root:Send to: C:5001/api/cache/move_keys with Paylod {'port': 5004, 'dest': {'A': ['k2']}}
INFO:root:Send to: D:5001/api/cache/move_keys with Paylod {'port': 5004, 'dest': {'B': ['k1']}}
```
[A, B] -> [A, B, D]
```
INFO:root:Old mapping: {0: 'A', 1: 'B', 2: 'A', 3: 'B', 4: 'A', 5: 'B', 6: 'A', 7: 'B', 8: 'A', 9: 'B', 10: 'A', 11: 'B', 12: 'A', 13: 'B', 14: 'A', 15: 'B'}
INFO:root:New mapping: {0: 'A', 1: 'B', 2: 'D', 3: 'A', 4: 'B', 5: 'D', 6: 'A', 7: 'B', 8: 'D', 9: 'A', 10: 'B', 11: 'D', 12: 'A', 13: 'B', 14: 'D', 15: 'A'}
INFO:root:Old-new mapping: {'A': [(2, 'D'), (4, 'B'), (8, 'D'), (10, 'B'), (14, 'D')], 'B': [(3, 'A'), (5, 'D'), (9, 'A'), (11, 'D'), (15, 'A')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'B', 'payload': {'port': -1, 'dest': {'D': ['k1']}}}]
INFO:root:Send to: B:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'D': ['k1']}}
```
[A, B, C, D] -> [A, B]
```
INFO:root:Old mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'A', 9: 'B', 10: 'C', 11: 'D', 12: 'A', 13: 'B', 14: 'C', 15: 'D'}
INFO:root:New mapping: {0: 'A', 1: 'B', 2: 'A', 3: 'B', 4: 'A', 5: 'B', 6: 'A', 7: 'B', 8: 'A', 9: 'B', 10: 'A', 11: 'B', 12: 'A', 13: 'B', 14: 'A', 15: 'B'}
INFO:root:Old-new mapping: {'C': [(2, 'A'), (6, 'A'), (10, 'A'), (14, 'A')], 'D': [(3, 'B'), (7, 'B'), (11, 'B'), (15, 'B')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'C', 'payload': {'port': 5004, 'dest': {'A': ['k2']}}}, {'send_to': 'D', 'payload': {'port': 5004, 'dest': {'B': ['k1']}}}]
INFO:root:Send to: C:5001/api/cache/move_keys with Paylod {'port': 5004, 'dest': {'A': ['k2']}}
INFO:root:Send to: D:5001/api/cache/move_keys with Paylod {'port': 5004, 'dest': {'B': ['k1']}}
```
[A, B] -> [A, B, C, D]
```
INFO:root:Old mapping: {0: 'A', 1: 'B', 2: 'A', 3: 'B', 4: 'A', 5: 'B', 6: 'A', 7: 'B', 8: 'A', 9: 'B', 10: 'A', 11: 'B', 12: 'A', 13: 'B', 14: 'A', 15: 'B'}
INFO:root:New mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'A', 9: 'B', 10: 'C', 11: 'D', 12: 'A', 13: 'B', 14: 'C', 15: 'D'}
INFO:root:Old-new mapping: {'A': [(2, 'C'), (6, 'C'), (10, 'C'), (14, 'C')], 'B': [(3, 'D'), (7, 'D'), (11, 'D'), (15, 'D')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'A', 'payload': {'port': -1, 'dest': {'C': ['k2']}}}, {'send_to': 'B', 'payload': {'port': -1, 'dest': {'D': ['k1']}}}]
INFO:root:Send to: A:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'C': ['k2']}}
INFO:root:Send to: B:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'D': ['k1']}}
```
[A, B, C, D] -> [C, D]
```
INFO:root:Old mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'A', 9: 'B', 10: 'C', 11: 'D', 12: 'A', 13: 'B', 14: 'C', 15: 'D'}
INFO:root:New mapping: {0: 'C', 1: 'D', 2: 'C', 3: 'D', 4: 'C', 5: 'D', 6: 'C', 7: 'D', 8: 'C', 9: 'D', 10: 'C', 11: 'D', 12: 'C', 13: 'D', 14: 'C', 15: 'D'}
INFO:root:Old-new mapping: {'A': [(0, 'C'), (4, 'C'), (8, 'C'), (12, 'C')], 'B': [(1, 'D'), (5, 'D'), (9, 'D'), (13, 'D')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'A', 'payload': {'port': 5004, 'dest': {'C': ['test', 'test123', 'testabc']}}}, {'send_to': 'B', 'payload': {'port': 5004, 'dest': {}}}]
INFO:root:Send to: A:5001/api/cache/move_keys with Paylod {'port': 5004, 'dest': {'C': ['test', 'test123', 'testabc']}}
INFO:root:Send to: B:5001/api/cache/move_keys with Paylod {'port': 5004, 'dest': {}}
```
[C, D] -> [A, B, C, D]
```
INFO:root:Old mapping: {0: 'C', 1: 'D', 2: 'C', 3: 'D', 4: 'C', 5: 'D', 6: 'C', 7: 'D', 8: 'C', 9: 'D', 10: 'C', 11: 'D', 12: 'C', 13: 'D', 14: 'C', 15: 'D'}
INFO:root:New mapping: {0: 'C', 1: 'D', 2: 'A', 3: 'B', 4: 'C', 5: 'D', 6: 'A', 7: 'B', 8: 'C', 9: 'D', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'A', 15: 'B'}
INFO:root:Old-new mapping: {'C': [(2, 'A'), (6, 'A'), (10, 'A'), (14, 'A')], 'D': [(3, 'B'), (7, 'B'), (11, 'B'), (15, 'B')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'C', 'payload': {'port': -1, 'dest': {'A': ['k2']}}}, {'send_to': 'D', 'payload': {'port': -1, 'dest': {'B': ['k1']}}}]
INFO:root:Send to: C:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'A': ['k2']}}
INFO:root:Send to: D:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'B': ['k1']}}
```
[A, B, C, D] -> [B, C, D]
```
INFO:root:Old mapping: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'A', 9: 'B', 10: 'C', 11: 'D', 12: 'A', 13: 'B', 14: 'C', 15: 'D'}
INFO:root:New mapping: {0: 'B', 1: 'C', 2: 'D', 3: 'B', 4: 'C', 5: 'D', 6: 'B', 7: 'C', 8: 'D', 9: 'B', 10: 'C', 11: 'D', 12: 'B', 13: 'C', 14: 'D', 15: 'B'}
INFO:root:Old-new mapping: {'A': [(0, 'B'), (4, 'C'), (8, 'D'), (12, 'B')], 'B': [(1, 'C'), (5, 'D'), (13, 'C')], 'C': [(2, 'D'), (6, 'B'), (14, 'D')], 'D': [(3, 'B'), (7, 'C'), (15, 'B')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'A', 'payload': {'port': 5004, 'dest': {'B': ['test', 'test123', 'testabc']}}}, {'send_to': 'C', 'payload': {'port': -1, 'dest': {'B': ['k2']}}}]
INFO:root:Send to: A:5001/api/cache/move_keys with Paylod {'port': 5004, 'dest': {'B': ['test', 'test123', 'testabc']}}
INFO:root:Send to: C:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'B': ['k2']}}
```
[B, C, D] -> [A, B, C, D]
```
INFO:root:Old mapping: {0: 'B', 1: 'C', 2: 'D', 3: 'B', 4: 'C', 5: 'D', 6: 'B', 7: 'C', 8: 'D', 9: 'B', 10: 'C', 11: 'D', 12: 'B', 13: 'C', 14: 'D', 15: 'B'}
INFO:root:New mapping: {0: 'B', 1: 'C', 2: 'D', 3: 'A', 4: 'B', 5: 'C', 6: 'D', 7: 'A', 8: 'B', 9: 'C', 10: 'D', 11: 'A', 12: 'B', 13: 'C', 14: 'D', 15: 'A'}
INFO:root:Old-new mapping: {'B': [(3, 'A'), (6, 'D'), (9, 'C'), (15, 'A')], 'C': [(4, 'B'), (7, 'A'), (10, 'D')], 'D': [(5, 'C'), (8, 'B'), (11, 'A')]}
INFO:root:Current cached keys: {0: {'test'}, 12: {'test123', 'testabc'}, 11: {'k1'}, 6: {'k2'}}
INFO:root:Balance result: [{'send_to': 'B', 'payload': {'port': -1, 'dest': {'D': ['k2']}}}, {'send_to': 'D', 'payload': {'port': -1, 'dest': {'A': ['k1']}}}]
INFO:root:Send to: B:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'D': ['k2']}}
INFO:root:Send to: D:5001/api/cache/move_keys with Paylod {'port': -1, 'dest': {'A': ['k1']}}
```
## TODO
- [x] Remove functionality to configure memcache settings.
- [x] Remove functionality that displays memcache statistics.
- [x] All image files should be stored in S3.
- [x] The mapping between keys and image files should be stored in AWS RDS. Do not store the images themselves in the RDS database.
- [x] Route requests to the memcache pool using a consistent hashing approach based on MD5 hashes. For simplicity, assume that the key space is partitioned into 16 equal-size regions which are then allocated to the pool of memcache nodes. Figures 1-3 illustrate how this assignment changes as the pool size changes from one node to two nodes to three nodes More information changes as the pool size changes from one node to two nodes, to three nodes. More information is provided in the Consistent Hashing section below.
  - [x] find_location(cur_node_num, find_partition(key))
  - [x] Moving keys and values before cache access if pool size changed, "The assignment of key values to nodes changes each time a new node is added or removed, so ensure that you are updating nodes each time". (added by Teng Shu)
    - you move images whenever memcache nodes are added or removed, according to the new assignment of images to nodes (following the hashing shown in the assignment).
    - balance?
    - new api in manager to lock inc/desc until re-balance is done?
- [x] Add a feature to the front-end that allows the front-end to be automatically notified when the size of the memcache pool changes. In response, the front-end should rebalance the mapping of key regions to nodes, and use the new allocation to route requests to the memcache
  - [x] new endpoint
  - [x] balance
- [ ] Integration
