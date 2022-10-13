import mysql
from memcache_Shawn.memcache.app.db_operations.db_connection import connect_to_db


def get_replacement_policy_db():
    cnx = connect_to_db()
    cursor = cnx.cursor()

    query = "SELECT `value` FROM config ORDER BY id LIMIT 1"
    cursor.execute(query)
    replacement_policy = cursor.fetchall()
    return replacement_policy[0][0]

    cursor.close()
    cnx.close()


def get_capacity_in_mb_db():
    cnx = connect_to_db()
    cursor = cnx.cursor()

    query = "SELECT `value` FROM config ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    capacity_in_mb = cursor.fetchall()
    return capacity_in_mb[0][0]

    cursor.close()
    cnx.close()
