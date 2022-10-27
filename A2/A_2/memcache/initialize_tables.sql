-- ! initialize statistics_10min
DELETE FROM status WHERE id >= 0;

DELETE FROM key_image WHERE id >= 0;

UPDATE config SET `value` = '1' WHERE `key` = 'capacity';
UPDATE config SET `value` = 'lru' WHERE `key` = 'policy';
