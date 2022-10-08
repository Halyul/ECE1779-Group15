import app


def get_least_recently_used_key_db():
    query = "SELECT key_value FROM cache_keys ORDER BY time_last_used LIMIT 1"
    app.cursor.execute(query)
    for key_value in app.cursor:
        return key_value


def get_image_size_db(key):
    query = "SELECT image_size FROM cache_keys WHERE key_value = %s"
    app.cursor.execute(query, key)
    for image_size in app.cursor:
        return image_size


def update_time_last_used_db(current_time, key):
    query = "UPDATE cache_keys SET time_last_used = %s WHERE key_value = %s"
    app.cursor.execute(query, (current_time, key))
    app.cnx.commit()


def delete_key_db(key):
    query = "DELETE FROM cache_keys WHERE key_value = %s"
    app.cursor.execute(query, key)
    app.cnx.commit()


def delete_all_keys_db():
    query = "DELETE FROM cache_keys"
    app.cursor.execute(query)
    app.cnx.commit()
