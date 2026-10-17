from pipeline.checks import validate_rows
from pipeline.transform import clean_events, get_region


def make_feature(event_id="us1", mag=4.5, place="10 km S of Somewhere, Chile"):
    return {
        "id": event_id,
        "properties": {
            "mag": mag,
            "place": place,
            "time": 1760000000000,
            "type": "earthquake",
            "url": "https://example.com/" + event_id,
        },
        "geometry": {"coordinates": [-70.5, -33.4, 25.0]},
    }


def test_region_is_text_after_last_comma():
    assert get_region("10 km S of Somewhere, Chile") == "Chile"


def test_region_without_comma_is_whole_place():
    assert get_region("Mid-Atlantic Ridge") == "Mid-Atlantic Ridge"


def test_region_handles_missing_place():
    assert get_region(None) == "Unknown"


def test_events_without_magnitude_are_dropped():
    rows = clean_events([make_feature(mag=None), make_feature(event_id="us2")])
    assert len(rows) == 1
    assert rows[0]["event_id"] == "us2"


def test_duplicate_ids_are_removed():
    rows = clean_events([make_feature(), make_feature()])
    good_rows, problems = validate_rows(rows)
    assert len(good_rows) == 1
    assert len(problems) == 1


def test_impossible_latitude_is_rejected():
    feature = make_feature()
    feature["geometry"]["coordinates"] = [10.0, 95.0, 5.0]
    good_rows, problems = validate_rows(clean_events([feature]))
    assert good_rows == []
    assert len(problems) == 1