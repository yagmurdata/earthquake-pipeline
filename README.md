# Earthquake Pipeline

A small data pipeline that pulls the last 24 hours of earthquakes from the USGS API, cleans and checks the data, and saves it into a Postgres database. Everything runs in Docker.

## Why I built this

[Write one or two sentences in your own words: why earthquakes, and what you wanted to practice.]

## How it works

USGS API → extract → transform → checks → load → PostgreSQL

- `pipeline/extract.py` requests earthquakes (magnitude 2.5 and above) from the last 24 hours.
- `pipeline/transform.py` turns the raw data into clean rows: readable column names, UTC timestamps, and a region taken from the place name. Events without a magnitude are dropped.
- `pipeline/checks.py` skips duplicate events and values outside realistic ranges (for example a latitude above 90), and prints what it skipped.
- `pipeline/load.py` creates the table if it doesn't exist and saves the rows. If an event is already in the table, it is updated instead of duplicated.
- `pipeline/main.py` runs these steps in order.
- `tests/test_transform.py` has pytest tests for the cleaning and checking steps.
- `queries.sql` has example SQL queries to explore the data.

A few choices I made:

- The load step uses an upsert (`ON CONFLICT DO UPDATE`), so running the pipeline twice doesn't create duplicates. USGS also revises events after the fact, so updating makes sense.
- The database password is in a `.env` file that is not committed to GitHub.
- The script retries the database connection for a few seconds, because Postgres needs a moment to start.

## Tech

Python 3.11, PostgreSQL 16, Docker Compose, pytest, requests, psycopg2.

## How to run

You need Docker Desktop installed and running.

1. Clone the repo:

```
git clone https://github.com/yourusername/earthquake-pipeline.git
cd earthquake-pipeline
```

2. Create your settings file and choose your own password inside it:

```
cp .env.example .env
```

3. Start the database and run the pipeline:

```
docker compose up --build -d
```

4. Check the output:

```
docker compose logs pipeline
```

5. Run the tests:

```
docker compose run --rm pipeline python -m pytest
```

6. Run the example queries:

```
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < queries.sql
```

7. Run the pipeline again whenever you want new data:

```
docker compose run --rm pipeline
```

8. Stop everything (your data is kept):

```
docker compose down
```

Use `docker compose down -v` instead if you also want to delete the data.

## Example output

[Paste a few lines of your own output here, like the "Fetched ... events" and "Loaded ... events" lines, or one result from queries.sql.]

## Project structure

```
earthquake-pipeline/
├── pipeline/
│   ├── extract.py
│   ├── transform.py
│   ├── checks.py
│   ├── load.py
│   └── main.py
├── tests/
│   └── test_transform.py
├── queries.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## What I learned

- Docker Compose only reads a file named exactly `.env`, so I needed both `.env` (my real settings) and `.env.example` (the template on GitHub).
- Docker Desktop has to be running before any `docker compose` command works.
- VS Code shows import warnings for `psycopg2` because the library is installed inside the container, not on my Mac.
- [Add your own: something that went wrong for you and how you fixed it.]

## Limitations and next steps

- It only fetches the last 24 hours, and I have to run it by hand. There is no scheduling yet.
- It only prints messages and has no proper logging.
- The checks assume every event has a depth value.
- Next steps: schedule it with Airflow, keep history to look at trends over time, and add a simple dashboard.

## Data source

Earthquake data comes from the [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/fdsnws/event/1/).
