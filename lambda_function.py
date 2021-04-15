from NearestStationORM.controller import Controller
from WalkingDistanceAPI.controller import get_distance

import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV = "staging"

def update_nearby_station_info(pnu, ctl):
    article_coord = ctl.get_article_coord(pnu)
    if article_coord.__len__() == 0:
        logger.info("There is no article")
        return

    station = ctl.find_nearby_station(pnu)
    if station["lat"] is None:
        logger.info("There is no near station")
        return

    distance = get_distance(article_coord, station)

    near_by_station_data = aggregation_nearby_station(pnu, station, distance)

    envs = ["staging", "production"]
    for env in envs:
        save_nearby_station_info(near_by_station_data, env)


def aggregation_nearby_station(pnu: str, station: dict, distance: dict) -> dict:
    data = dict()
    data["pnu"] = pnu
    data["station_id"] = station["id"]
    data["station_line"] = station["line"]
    data["station_name"] = station["name"]
    data["distance"] = distance["distance"]
    data["consuming_time"] = distance["consuming_time"]
    data["route"] = distance["route"]
    return data


def save_nearby_station_info(data: dict, env: str) :
    ctl = Controller(env)
    if data["consuming_time"] < 21:
        results = ctl.save_nearby_station_info(data)
        logger.info(results)
        return {
            'results': results
        }
    else:
        logger.info("too far to walk")


def lambda_handler(event, context):
    ctl = Controller(ENV)

    pnus = pick_target_to_nearby_station(event, ctl)

    for pnu in pnus:
        update_nearby_station_info(pnu, ctl)

    logger.info("update completed")

    return {
        'statusCode': 200,
        'body': pnus
    }


def pick_target_to_nearby_station(event, ctl):
    if event is None or "pnu" not in event or event["pnu"] is None:
        pnus = ctl.get_pnus()
    else:
        pnus = event['pnu']
        logger.info("requested : " + json.dumps(pnus))

    existed = ctl.get_pnus_having_subway_info()

    if type(pnus) is str:
        pnus = [pnus]

    return list(set(pnus).difference(set(existed)))


def main():
    event = dict()
    event["env"] = "local"
    lambda_handler(event, None)


if __name__ == '__main__':
    main()
