from memcache_Shawn.memcache.app.db_operations.db_connection import connect_to_db


def store_stats_db(cache_nums, cache_used_size, req_nums, total_hit, hit_rate, miss_rate):
    cnx = connect_to_db()
    cursor = cnx.cursor()

    query = ("INSERT INTO cache_stats"
             "(cache_nums, used_size, total_request_served, total_hit, miss_rate, hit_rate) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
    query_data = (cache_nums, cache_used_size, req_nums, total_hit, hit_rate, miss_rate)
    cursor.execute(query, query_data)

    cnx.commit()

    cursor.close()
    cnx.close()
