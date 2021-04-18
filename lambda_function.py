from NearestStationORM.controller import Controller
from WalkingDistanceAPI.controller import get_distance

import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV = "staging"


def get_nearby_station_info(pnus: list, ctl):
    info_datas = list()
    for pnu in pnus:
        article_coord = ctl.get_article_coord(pnu)
        if len(article_coord) == 0:
            logger.info("There is no article")
            continue

        station = ctl.find_nearby_station(pnu)
        if station["lat"] is None:
            logger.info("There is no near station")
            continue

        distance = get_distance(article_coord, station)

        info_datas.append(aggregation_nearby_station(pnu, station, distance))

    if len(info_datas) == 0:
        return

    envs = ["staging", "production"]
    for env in envs:
        save_nearby_station_info(info_datas, env)


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


def save_nearby_station_info(datas: list, env: str):
    ctl = Controller(env)
    for data in datas:
    # if data["consuming_time"] < 21:
        results = ctl.save_nearby_station_info(data)
        logger.info(results)
    # else:
    #     logger.info("too far to walk")


def lambda_handler(event, context):
    ctl = Controller(ENV)

    pnus = pick_target_to_nearby_station(event, ctl)
    logger.info("size of pnu list without station info : " + str(len(pnus)))

    for i in range(0, len(pnus), 100):
        get_nearby_station_info(pnus[i:i + 100], ctl)

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
    lambda_handler(event, None)


if __name__ == '__main__':
    main()
