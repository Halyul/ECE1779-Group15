import app


def store_stats_db(time_created, cache_nums, cache_size, req_nums, hit_rate, miss_rate):
    query = ("INSERT INTO cache_stats"
             "(time_created, cache_nums, cache_size, req_nums, miss_rate, hit_rate) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
    query_data = (time_created, cache_nums, cache_size, req_nums, miss_rate, hit_rate)
    app.cursor.execute(query, query_data)
    app.cnx.commit()
