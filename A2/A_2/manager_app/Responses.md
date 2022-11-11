GET /api/manager/pool_node_list
```json
{
	"pool_node_list": ["ip1", "ip2", "ip3"]
}
```


GET /api/manager/poolsize/config -> UI
```json
{
	"resize_pool_option": "automatic",
	"resize_pool_parameters": {
		"max_miss_rate_threshold": 1,
		"min_miss_rate_threshold": 1,
		"ratio_expand_pool": 1,
		"ratio_shrink_pool": 1,
		"auto_mode": "true"
	}
}
```

GET /api/manager/aggregate_stats -> UI
```json
{
	"miss_rate": [],
	"hit_rate": [], 
	"number_of_items_in_cache": [],
	"total_size_of_items_in_cache": [],
	"number_of_requests_served_per_minute": []
}
```

GET /api/manager/poolsize
```json
{
	"size": 1
}
```

GET /api/manager/cache/config -> UI
```json
{
	"capacity": 100,
	"replacement_policy": "Random Replacement"
}
```

POST /api/manager/poolsize/manual -> UI
```json
{
	"success": "true",
    "content": response of POST /api/pool_size_change from instance 1 <- ?
}
```

```json
{
	"success": "false",
        "error": {
            "code": 400,
            "message": "The size of memcache pool has been reached to maximum"
        }
}
```
```json
{
	"success": "false",
        "error": {
            "code": 400,
            "message": "The size of memcache pool has been reached to minimum"
        }
}
```
```json
{
	"success": "false",
        "error": {
            "code": 400,
            "message": "Parameter change can only be increase or decrease"
        }
}
```
POST /api/poolsize/change -> UI
```json
{
	"success": "true",
    "content": "Memcache pool size increases"
}
```

```json
{
	"success": "true",
    "content": "Memcache pool size decreases"
}
```

POST /api/manager/poolsize/automatic -> UI

```json
{
	"success": "true",
    "content": response of POST /api/scaler/config from auto scalar
}
```

POST /api/manager/cache/config -> UI
```json
{
	"success": "true",
    "content": response of POST /api/cache/config from instance 2
}
```

DELETE /api/manager/cache/clear -> UI
```json
{
	"success": "true",
    "content": [response of node1 DELETE /api/cache from instance 2, response of node2 DELETE /api/cache from instance 2, ...]
}
```

DELETE /api/manager/data/clear -> UI
```json
{
	"success": "true",
    "content": "All data are successfully deleted"
}
```
