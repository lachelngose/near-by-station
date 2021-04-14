import requests
import time
import logging

from WalkingDistanceAPI.config import API_KEY

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BASE_URL = "https://apis.openapi.sk.com/tmap/routes/pedestrian"


def make_request(payload: dict):
    params = {'version': '1', 'callback': 'json'}
    headers = {'appKey': API_KEY}
    logger.info(payload)

    max_try_count = 5
    try_count = 0

    while try_count < max_try_count:
        response = requests.post(BASE_URL, params=params, data=payload, headers=headers)
        print(response.status_code)

        if response.status_code / 100 == 2:
            return response.json()
        elif response.status_code == 403:
            time.sleep(5)
            try_count += 1

    response.reason = response.text
    response.raise_for_status()