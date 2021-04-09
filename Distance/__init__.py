import time
import urllib.error
import urllib.parse
import urllib.request

from Distance.config import API_KEY


BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"


def make_request(origins, destinations):
    for dest in destinations:
        params = urllib.parse.urlencode(
            {"origins": f"{origins}", "destinations": f"{dest}", "mode": "walking", "key": API_KEY}
        )
        url = f"{BASE_URL}?{params}"

        current_delay = 0.1
        max_delay = 5

        while True:
            try:
                response = urllib.request.urlopen(url)
            except urllib.error.URLError:
                pass
            else:
                return response

            if current_delay > max_delay:
                raise Exception("Too many retry attempts.")

            print("Waiting", current_delay, "seconds before retrying.")

            time.sleep(current_delay)
            current_delay *= 2
