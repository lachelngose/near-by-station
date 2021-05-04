from NearestStationORM.controller import Controller
from WalkingDistanceAPI.controller import get_distance

import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENV = "staging"

def get_distance_to_point(pnus: list, ctl):
    info_datas, updated_pnus = get_nearby_station_info(pnus, ctl)

    remained_pnus = list(set(pnus).difference(set(updated_pnus)))
    info_datas.extend(get_route_station_info(remained_pnus, ctl))

    envs = ["local"]
    for env in envs:
        save_nearby_station_info(info_datas, env)


def get_nearby_station_info(pnus: list, ctl):
    info_datas = list()
    updated_pnus = list()
    for pnu in pnus:
        article_coord = ctl.get_article_coord(pnu)
        if len(article_coord) == 0:
            logger.info("There is no article")
            continue

        station = ctl.find_nearby_station(1000, pnu)
        if station["lat"] is None:
            logger.info('There is no station close to ' + str(pnu))
            continue

        distance = get_distance(article_coord, station, True)

        info_data = aggregation_info_data(pnu, station, distance)
        logger.info(info_data)
        info_datas.append(info_data)

        if info_data['consuming_time'] < 16:
            updated_pnus.append(pnu)

    return info_datas, updated_pnus


def get_route_station_info(pnus: list, ctl):
    info_datas = list()
    for pnu in pnus:
        article_coord = ctl.get_article_coord(pnu)
        if len(article_coord) == 0:
            logger.info("There is no article")
            continue

        station = ctl.find_nearby_station(10000, pnu)

        distance = get_distance(article_coord, station, False)

        info_data = aggregation_info_data(pnu, station, distance)
        logger.info(info_data)
        info_datas.append(info_data)

    return info_datas


def aggregation_info_data(pnu: str, station: dict, distance: dict) -> dict:
    data = dict()
    data["pnu"] = pnu
    data["station_id"] = station["id"]
    data["station_line"] = station["line"]
    data["station_name"] = station["name"]
    data["distance"] = distance["distance"]
    data["travel_mode"] = distance["travel_mode"]
    data["consuming_time"] = distance["consuming_time"]
    data["route"] = distance["route"]
    return data


def save_nearby_station_info(datas: list, env: str):
    ctl = Controller(env)
    for data in datas:
        results = ctl.save_nearby_station_info(data)
        logger.info(results)


def lambda_handler(event, context):
    ctl = Controller(ENV)

    pnus = pick_target_to_nearby_station(event, ctl)
    logger.info("size of pnu list without station info : " + str(len(pnus)))

    for i in range(0, len(pnus), 100):
        get_distance_to_point(pnus[i:i + 100], ctl)

    logger.info("update completed")

    return {
        'statusCode': 200,
        'body': pnus
    }


def pick_target_to_nearby_station(event, ctl):
    if event is None or "pnu" not in event or event["pnu"] is None:
        pnus = ctl.get_pnus()
    else:
        requested = event['pnu']
        logger.info("requested : " + json.dumps(event['pnu']))
        if type(requested) is str:
            requested = [requested]

        pnus = list(filter(ctl.is_article_exist, requested))
        logger.info("targeted : " + json.dumps(pnus))

    existed = ctl.get_pnus_having_subway_info()

    return list(set(pnus).difference(set(existed)))


def main():
    event = dict()
    lambda_handler(event, None)


if __name__ == '__main__':
    main()
