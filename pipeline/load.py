import os
import time

import psycopg2
from psycopg2.extras import execute_values

COLUMNS = [
    "event_id", "occurred_at", "magnitude", "place", "region",
    "latitude", "longitude", "depth_km", "event_type", "url",
]

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS earthquakes (
    event_id TEXT PRIMARY KEY,
    occurred_at TIMESTAMPTZ NOT NULL,
    magnitude DOUBLE PRECISION NOT NULL,
    place TEXT,
    region TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    depth_km DOUBLE PRECISION,
    event_type TEXT,
    url TEXT
)
"""


INSERT = f"""
INSERT INTO earthquakes ({", ".join(COLUMNS)})
VALUES %s
ON CONFLICT (event_id) DO UPDATE SET
    magnitude = EXCLUDED.magnitude,
    place = EXCLUDED.place,
    region = EXCLUDED.region
"""


def get_connection():
    for attempt in range(10):
        try:
            return psycopg2.connect(
                host=os.environ["DB_HOST"],
                port=os.environ.get("DB_PORT", "5432"),
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
        except psycopg2.OperationalError:
            print(f"Database not ready, retrying ({attempt + 1}/10)...")
            time.sleep(2)
    raise RuntimeError("Could not connect to the database")


def load_rows(rows):
    if not rows:
        return 0
    values = [tuple(row[col] for col in COLUMNS) for row in rows]
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE)
            execute_values(cur, INSERT, values)
    conn.close()
    return len(values)