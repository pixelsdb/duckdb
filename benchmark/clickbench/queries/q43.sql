SELECT date_trunc('minute'::VARCHAR, CAST(EventTime AS TIMESTAMP)) AS M, COUNT(*) AS PageViews
FROM hits
WHERE CounterID = 62
  AND EventDate >= '2013-07-14'
  AND EventDate <= '2013-07-15'
  AND IsRefresh = 0
  AND DontCountHits = 0
GROUP BY date_trunc('minute'::VARCHAR, CAST(EventTime AS TIMESTAMP))
ORDER BY date_trunc('minute'::VARCHAR, CAST(EventTime AS TIMESTAMP))
    LIMIT 10 OFFSET 1000;