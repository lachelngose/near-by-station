from sqlalchemy.exc import SQLAlchemyError
import logging

import NearestStationORM
from NearestStationORM.config import *
from NearestStationORM.entity import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Controller:

    def __init__(self, env: str):
        dbinfo = get_dbinfo_by_env(env)
        logger.info("try to connect database : " + dbinfo["name"])

        self.dal = NearestStationORM.create_database_layer(
            DB_DRIVER=dbinfo["driver"],
            DB_HOST=dbinfo["host"],
            DB_NAME=dbinfo["name"],
            DB_USER=dbinfo["user"],
            DB_PASSWORD=dbinfo["password"],
            DB_PORT=dbinfo["port"]
        )

        logger.info("data access layer created.")

    def get_article_coord(self, pnu: str) -> dict:
        rs = self.dal.session.query(Article.lat, Article.lng).filter_by(pnu=pnu).first()
        if rs is None:
            return dict()
        return dict(rs)

    def get_pnus_having_subway_info(self):
        rs = self.dal.session.query(Article.pnu).distinct(Article.pnu)\
            .join(NearByStationInfo, Article.pnu == NearByStationInfo.pnu).all()
        return map(lambda a: a[0], rs)

    def get_pnus(self):
        rs = self.dal.session.query(Article.pnu).distinct(Article.pnu).all()
        return map(lambda a: a[0], rs)

    def find_nearby_station(self, pnu: str) -> Station:
        sql = ("SELECT s.id, s.line, s.name, s.lat, s.lng\n"
               "FROM article_master a\n"
               "LEFT JOIN station_coordinate s\n"
               "    ON ST_DWithin(\n"
               "          ST_Transform(ST_SetSRID(ST_MakePoint(a.longitude, a.latitude), 4326),5186), \n"
               "          ST_Transform(ST_SetSRID(ST_MakePoint(s.lng, s.lat), 4326),5186), 1000) \n"
               "WHERE a.pnu = \'{pnu}\'"
               "ORDER BY ST_Distance(ST_MakePoint(a.longitude, a.latitude), ST_MakePoint(s.lng, s.lat))"
               "LIMIT 1").format(pnu=pnu)

        obj = self.dal.session.execute(sql).fetchone()
        return Station(obj[0], obj[1], obj[2], obj[3], obj[4])

    def save_nearby_station_info(self, data: dict):
        info_data = NearByStationInfo(data["pnu"], data["station_id"], data["station_line"], data["station_name"],
                                      data["distance"], data["consuming_time"], data["route"])

        try:
            self.dal.add_object(info_data)
            return "OK"
        except SQLAlchemyError:
            return SQLAlchemyError.code
