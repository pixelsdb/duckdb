SELECT
    UserID,
    extract(minute FROM EventTime::TIMESTAMP) AS m,
    SearchPhrase,
    COUNT(*)
FROM
    hits
GROUP BY
    UserID, m, SearchPhrase
ORDER BY
    COUNT(*) DESC
    LIMIT 10;
