from psycopg2.extensions import JSON


class Route:
    index: int
    geometry: dict
    properties: dict

    def __init__(self, feature: JSON):
        self.geometry = feature["geometry"]
        self.properties = feature["properties"]
        self.index = feature["properties"]["index"]


def convert_route_list(feature_collection: JSON):
    features = feature_collection["features"]
    route_list = list()
    for feature in features:
        route_list.append(Route(feature))

    return route_list


def get_total_distance(route_list: list):
    for route in route_list:
        if route.index == 0:
            return route.properties["totalDistance"]


def get_total_time(route_list: list):
    for route in route_list:
        if route.index == 0:
            return route.properties["totalTime"]
