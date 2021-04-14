from NearestStationORM.controller import Controller
from WalkingDistanceAPI.controller import get_distance

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def update_nearby_station_info(pnu, ctl):
    article_coord = ctl.get_article_coord(pnu)
    station = ctl.find_nearby_station(pnu)
    if station["lat"] is None:
        logger.info("There is no near station")
        return

    distance = get_distance(article_coord, station)

    near_by_station_data = aggregation_nearby_station(pnu, station, distance)

    results = ctl.save_nearby_station_info(near_by_station_data)
    logger.info(results)

    return {
        'results': results
    }


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


def lambda_handler(event, context):
    ctl = Controller(event["env"])

    pnus = pick_target_to_nearby_station(event, ctl)

    for pnu in pnus:
        update_nearby_station_info(pnu, ctl)


def pick_target_to_nearby_station(event, ctl):
    if event is None or "pnu" not in event or event["pnu"] is None:
        pnus = ctl.get_pnus()
    else:
        pnus = event['pnu']

    existed = ctl.get_pnus_having_subway_info()

    if type(pnus) is str:
        pnus = [pnus]

    return set(pnus).difference(set(existed))


def main():
    lambda_handler(None, None)


if __name__ == '__main__':
    main()
