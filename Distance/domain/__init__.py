from psycopg2.extensions import JSON


class Route:
    index: int
    geometry: dict

    def __init__(self, feature: JSON):
        self.geometry = feature["geometry"]
        self.index = feature["properties"]["index"]
