from datetime import datetime, timedelta, timezone

import requests

URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def fetch_earthquakes(days=1, min_magnitude=2.5):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    params = {
        "format": "geojson",
        "starttime": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": end.strftime("%Y-%m-%dT%H:%M:%S"),
        "minmagnitude": min_magnitude,
        "orderby": "time",
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()["features"]