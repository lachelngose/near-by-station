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

    near_by_station = aggregation_near_by_station(pnu, station, distance)

    return {
        'results': near_by_station
    }


class NearbyStation:
    pnu: str
    station_id: int
    station_line: str
    station_name: str
    distance: float
    consuming_time: int
    route: list

    def __init__(self, pnu, station_id, station_line, station_name, distance, consuming_time, route):
        self.pnu = pnu
        self.station_id = station_id
        self.station_line = station_line
        self.station_name = station_name
        self.distance = distance
        self.consuming_time = consuming_time
        self.route = route


def aggregation_near_by_station(pnu: str, station: dict, distance: dict):
    return NearbyStation(pnu, station["id"], station["line"], station["name"],
                         distance["distance"], distance["consuming_time"], distance["route_list"])


def lambda_handler(event, context):
    return main(event, context)


if __name__ == '__main__':
    main()
