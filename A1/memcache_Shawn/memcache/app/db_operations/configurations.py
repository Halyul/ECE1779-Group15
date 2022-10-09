import mysql
from memcache_Shawn.memcache.app.db_operations.db_connection import connect_to_db


def get_replacement_policy_db():
    cnx = connect_to_db()
    cursor = cnx.cursor()

    query = "SELECT `key` FROM cache_configs ORDER BY id LIMIT 1"
    cursor.execute(query)
    for replacement_policy in cursor:
        return replacement_policy[0]

    cursor.close()
    cnx.close()


def get_capacity_in_mb_db():
    cnx = connect_to_db()
    cursor = cnx.cursor()

    query = "SELECT `key` FROM cache_configs ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    for capacity_in_mb in cursor:
        return capacity_in_mb[0]

    cursor.close()
    cnx.close()
