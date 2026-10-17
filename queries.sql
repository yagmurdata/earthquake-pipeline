-- 1. Ten strongest earthquakes
SELECT occurred_at, magnitude, place
FROM earthquakes
ORDER BY magnitude DESC
LIMIT 10;

-- 2. Most active regions
SELECT region, COUNT(*) AS quakes, ROUND(AVG(magnitude)::numeric, 2) AS avg_magnitude
FROM earthquakes
GROUP BY region
ORDER BY quakes DESC
LIMIT 10;

-- 3. Quakes per hour
SELECT DATE_TRUNC('hour', occurred_at) AS hour, COUNT(*) AS quakes
FROM earthquakes
GROUP BY hour
ORDER BY hour;

-- 4. Average depth by magnitude band
SELECT FLOOR(magnitude) AS magnitude_band,
       COUNT(*) AS quakes,
       ROUND(AVG(depth_km)::numeric, 1) AS avg_depth_km
FROM earthquakes
GROUP BY magnitude_band
ORDER BY magnitude_band;

-- 5. Deep earthquakes
SELECT occurred_at, magnitude, depth_km, place
FROM earthquakes
WHERE depth_km > 300
ORDER BY depth_km DESC;