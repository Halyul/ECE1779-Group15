import app


def get_replacement_policy_db():
    query = "SELECT replacement_policy FROM cache_configs ORDER BY time_modified LIMIT 1"
    app.cursor.execute(query)
    for replacement_policy in app.cursor:
        return replacement_policy[0]


def get_capacity_in_mb_db():
    query = "SELECT capacity_in_mb FROM cache_configs ORDER BY time_modified LIMIT 1"
    app.cursor.execute(query)
    for capacity_in_mb in app.cursor:
        return capacity_in_mb[0]
