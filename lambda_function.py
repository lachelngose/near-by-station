from NearestStationORM.controller import Controller
from WalkingDistanceAPI.controller import get_distance


def main(event, context):
    ctl = Controller()
    pnu = event['pnu']

    article_coord = ctl.get_article_coord(pnu)
    station = ctl.find_nearby_station(pnu)
    distance = get_distance(article_coord, station)

    near_by_station_data = aggregation_near_by_station(pnu, station, distance)

    results = ctl.save_nearby_station_info(near_by_station_data)
    print(results)

    return {
        'results': results
    }


def aggregation_near_by_station(pnu: str, station: dict, distance: dict) -> dict:
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
    return main(event, context)
