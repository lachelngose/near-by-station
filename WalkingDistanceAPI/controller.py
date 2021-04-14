from psycopg2.extensions import JSON

from WalkingDistanceAPI import make_request
from WalkingDistanceAPI.domain import Route


def get_distance(start: dict, end: dict) -> dict:
	payload = dict()
	payload["startX"] = start["lng"]
	payload["startY"] = start["lat"]
	payload["endX"] = end["lng"]
	payload["endY"] = end["lat"]
	payload["startName"] = "start"
	payload["endName"] = "end"

	result = make_request(payload)
	return convert_dict(result)


def convert_dict(feature_collection: JSON) -> dict:
	features = feature_collection["features"]
	distance = dict()
	route_list = list()
	for feature in features:
		route = Route(feature)
		if route.index == 0:
			distance["distance"] = feature["properties"]["totalDistance"]
			distance["consuming_time"] = int(feature["properties"]["totalTime"]/60)
		route_list.append(route.__dict__)

	distance["route"] = route_list
	return distance
