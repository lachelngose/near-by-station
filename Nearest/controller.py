from sqlalchemy.exc import SQLAlchemyError

import Nearest
from Nearest.config import *
from Nearest.entity import *


class Controller:

    def __init__(self):
        self.dal = Nearest.create_database_layer(
            DB_DRIVER='postgresql',
            DB_HOST=DB_HOST,
            DB_NAME=DB_NAME,
            DB_USER=DB_USER,
            DB_PASSWORD=DB_PASSWD,
            DB_PORT=DB_PORT
        )

    def get_article_coord(self, pnu: str) -> dict:
        article = self.dal.session.query(Article).filter_by(pnu=pnu).first()
        coord_dict = dict()
        coord_dict["lat"] = str(article.latitude)
        coord_dict["lng"] = str(article.longitude)
        return coord_dict

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
