from album.aws.dynamoDB_common import db_get_stats_from_table, CAPACITY, IMAGE_NUMBER, USER_NUMBER, CALL_NUMBER

capacity_used = db_get_stats_from_table(CAPACITY)
total_number_of_images = db_get_stats_from_table(IMAGE_NUMBER)
total_number_of_active_users = db_get_stats_from_table(USER_NUMBER)
total_number_of_function_calls = db_get_stats_from_table(CALL_NUMBER)
