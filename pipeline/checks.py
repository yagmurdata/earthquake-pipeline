LIMITS = {
    "magnitude": (-2, 10),
    "latitude": (-90, 90),
    "longitude": (-180, 180),
    "depth_km": (-10, 800),
}


def validate_rows(rows):
    good_rows = []
    problems = []
    seen_ids = set()

    for row in rows:
        event_id = row["event_id"]

        if event_id in seen_ids:
            problems.append(f"{event_id}: duplicate event")
            continue

        bad_fields = [
            name for name, (low, high) in LIMITS.items()
            if not low <= row[name] <= high
        ]
        if bad_fields:
            problems.append(f"{event_id}: out of range -> {', '.join(bad_fields)}")
            continue

        seen_ids.add(event_id)
        good_rows.append(row)

    return good_rows, problems