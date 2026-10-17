from datetime import datetime, timezone


def get_region(place):
  
    if not place:
        return "Unknown"
    if "," in place:
        return place.split(",")[-1].strip()
    return place.strip()


def clean_event(feature):
    props = feature["properties"]
    lon, lat, depth = feature["geometry"]["coordinates"]
    return {
        "event_id": feature["id"],
        "occurred_at": datetime.fromtimestamp(props["time"] / 1000, tz=timezone.utc),
        "magnitude": props["mag"],
        "place": props["place"],
        "region": get_region(props["place"]),
        "latitude": lat,
        "longitude": lon,
        "depth_km": depth,
        "event_type": props["type"],
        "url": props["url"],
    }


def clean_events(features):
    rows = []
    for feature in features:
        if feature["properties"]["mag"] is None:
            continue
        rows.append(clean_event(feature))
    return rows