from NearestStationORM.db import dal


def create_database_layer(DB_DRIVER, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT):
    url = "{}://{}:{}@{}:{}/{}"
    url = url.format(DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    dal.db_init(url)
    dal.get_session()

    return dal
