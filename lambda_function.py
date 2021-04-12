from Nearest.controller import Controller
from Distance.controller import get_distance


# def main(event, context):
def main():
    ctl = Controller()
    # pnu = event['pnu']
    pnu = '1126010300103050023'

    article_coord = ctl.get_article_coord(pnu)
    station = ctl.find_nearby_station(pnu)
    distance = get_distance(article_coord, station)

    near_by_station_data = aggregation_near_by_station(pnu, station, distance)

    results = ctl.save_nearby_station_info(near_by_station_data)
    print(results)

    return {
        'results': results
    }


def aggregation_near_by_station(pnu: str, station: dict, distance: dict):
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


if __name__ == '__main__':
    main()
