-- US recount from the working table: granted utility patents filed since 1 Nov 1996, by origin and top owner names.
-- Origin rows overlap because a publication can have multiple owners. Never sum origin rows to calculate a distinct-publication share.
-- The union row calculates the Alcatel/Lucent share at publication level; saved CSV snapshots require a rerun to include it.
WITH us AS (
    SELECT DISTINCT publication_number, o AS owner
    FROM nokia_analytics.portfolio_30y, UNNEST(owners) AS o
    WHERE country_code = 'US'
      AND grant_date > 0
      AND SUBSTR(kind_code, 1, 1) IN ('A', 'B', 'E')
), c AS (
    SELECT publication_number, owner,
        CASE
            WHEN REGEXP_CONTAINS(UPPER(owner), r'TCL|VACUUM|OPTRONICS|KABEL|CABLE|FIBRES|ESPACE|TELSPACE|MOBILE COMM|RADIOTELEPHONE|SUBMARCOM|SUBMARINE|TRANSP SOLUTION|ALSTHOM|ALSTHOLM|ALTHOM|ALTSHOM|COMMISSARIAT|INRIA|LUCENT KK|^TRT ') THEN 'Needs review'
            WHEN UPPER(owner) LIKE '%INFINERA%' THEN 'Infinera'
            WHEN REGEXP_CONTAINS(UPPER(owner), r'SHANGH[AI]{2} BELL') THEN 'Shanghai Bell'
            WHEN REGEXP_CONTAINS(UPPER(owner), r'S[IE]{2}M[EA]NS') THEN 'Nokia Siemens Networks'
            WHEN REGEXP_CONTAINS(UPPER(owner), r'^LUCENT|ATT CORP LUCENT') THEN 'Lucent'
            WHEN REGEXP_CONTAINS(UPPER(owner), r'ALCATEL|LUCENT') THEN 'Alcatel and Alcatel-Lucent'
            WHEN UPPER(owner) LIKE '%NOKIA%' THEN 'Nokia'
            ELSE 'Other'
        END AS origin
    FROM us
)
SELECT 'origin' AS row_type, origin AS label,
    COUNT(DISTINCT publication_number) AS patents,
    COUNT(DISTINCT owner) AS names,
    CAST(NULL AS FLOAT64) AS share_of_unique_publications
FROM c
GROUP BY origin
UNION ALL
SELECT 'total', 'Unique patents', COUNT(DISTINCT publication_number), COUNT(DISTINCT owner), NULL
FROM c
UNION ALL
SELECT 'total', 'Listings', COUNT(*), COUNT(DISTINCT owner), NULL
FROM c
UNION ALL
SELECT 'union', 'Alcatel and Lucent distinct union',
    COUNT(DISTINCT IF(origin IN ('Alcatel and Alcatel-Lucent', 'Lucent'), publication_number, NULL)),
    COUNT(DISTINCT IF(origin IN ('Alcatel and Alcatel-Lucent', 'Lucent'), owner, NULL)),
    COUNT(DISTINCT IF(origin IN ('Alcatel and Alcatel-Lucent', 'Lucent'), publication_number, NULL)) / COUNT(DISTINCT publication_number)
FROM c
UNION ALL (
    SELECT 'name', owner, COUNT(DISTINCT publication_number), 1, NULL
    FROM c
    GROUP BY owner
    ORDER BY 3 DESC
    LIMIT 15
)
ORDER BY row_type, patents DESC;
