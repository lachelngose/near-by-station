from Nearest.controller import Controller
from Distance.controller import get_distance


def main(event, context):
# def main():
    ctl = Controller()
    pnu = event['pnu']
    # pnu = '1111010100100520127'

    article, article_coord = ctl.get_article(pnu)
    stations, stations_coord = ctl.find_nearby_station(pnu)

    distances = get_distance(article_coord, stations_coord)

    convert_near_by_station(stations, distances)

    return {
        'results': ''
    }


class NearbyStation:
    name: str
    line: str
    distance: float
    consumingTime: int


def convert_near_by_station(stations, distances):
    pass  # to_do...


def lambda_handler(event, context):
    return main(event, context)


# if __name__ == '__main__':
#    main()
