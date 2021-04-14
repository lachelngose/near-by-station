def get_dbinfo_by_env(env: str) -> dict:
    dbinfo = dict()
    dbinfo["user"] = ""
    dbinfo["password"] = ""
    dbinfo["driver"] = ""
    dbinfo["port"] = ""
    if env == 'production':
        dbinfo["host"] = ""
        dbinfo["name"] = ""
    elif env == 'staging' :
        dbinfo["host"] = ""
        dbinfo["name"] = ""
    else:
        dbinfo["host"] = ""
        dbinfo["name"] = ""

    return dbinfo