-- ! initialize statistics_10min
DELETE FROM statistics_10min WHERE time > '0';

UPDATE statistics
SET num_item_in_cache = 0, used_size = 0, total_request_served = 0, total_hit = 0, miss_rate = NULL, hit_rate = NULL
WHERE id = 1;

UPDATE config SET `value` = '1' WHERE `key` = 'capacity';
UPDATE config SET `value` = 'rr' WHERE `key` = 'policy';
