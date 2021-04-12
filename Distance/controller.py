from Distance import make_request
from Distance import domain


def get_distance(start, end):
	payload = dict()
	payload["startX"] = start["lng"]
	payload["startY"] = start["lat"]
	payload["endX"] = end["lng"]
	payload["endY"] = end["lat"]
	payload["startName"] = "start"
	payload["endName"] = "end"

	result = make_request(payload)
	route_list = domain.convert_route_list(result)

	distance = dict()
	distance["distance"] = domain.get_total_distance(route_list)
	distance["consuming_time"] = domain.get_total_time(route_list)
	distance["route_list"] = route_list
	return distance
