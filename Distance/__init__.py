import requests

from Distance.config import API_KEY


BASE_URL = "https://apis.openapi.sk.com/tmap/routes/pedestrian"


def make_request(payload):
    params = {'version': '1', 'callback': 'json'}
    headers = {'appKey': API_KEY}

    response = requests.post(BASE_URL, params=params, data=payload, headers=headers)
    response.raise_for_status()

    return response.json()
