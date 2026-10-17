from pipeline.checks import validate_rows
from pipeline.extract import fetch_earthquakes
from pipeline.load import load_rows
from pipeline.transform import clean_events


def main():
    features = fetch_earthquakes(days=1, min_magnitude=2.5)
    print(f"Fetched {len(features)} events")

    rows = clean_events(features)
    good_rows, problems = validate_rows(rows)
    for problem in problems:
        print("Skipped:", problem)

    count = load_rows(good_rows)
    print(f"Loaded {count} events")


if __name__ == "__main__":
    main()