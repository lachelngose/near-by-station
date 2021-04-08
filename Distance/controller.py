import json

from Distance import make_request


def get_distance(origin, destinations):
    origin_str = origin["lat"] + "," + origin["lng"]
    dest_str_list = []

    for dest in destinations:
        dest_str_list.append(dest["lat"] + "," + dest["lng"])

    result = json.load(make_request(origin_str, "|".join(dest_str_list)))

    if result["status"] == "OK":
        return result["rows"]
    elif result["status"] != "UNKNOWN_ERROR":
        raise Exception(result["error_message"])
