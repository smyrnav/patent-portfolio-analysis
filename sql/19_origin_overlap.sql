-- Quantifies the double-counting in the old 46% figure: how many distinct US granted
-- publications (filed since 1 Nov 1996) carry both an Alcatel-group and a Lucent owner name.
-- Uses the same origin CASE as 08_recount_us_30y.sql, aggregated per publication.
-- Applicant/assignee names at filing, not verified current ownership.
WITH us AS (
    SELECT DISTINCT publication_number, o AS owner
    FROM nokia_analytics.portfolio_30y, UNNEST(owners) AS o
    WHERE country_code = 'US'
      AND grant_date > 0
      AND SUBSTR(kind_code, 1, 1) IN ('A', 'B', 'E')
), c AS (
    SELECT publication_number,
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
), per_patent AS (
    SELECT publication_number,
        MAX(origin = 'Alcatel and Alcatel-Lucent') AS has_alcatel_group,
        MAX(origin = 'Lucent') AS has_lucent
    FROM c
    GROUP BY publication_number
)
SELECT
    COUNT(*) AS unique_patents,
    COUNTIF(has_alcatel_group) AS alcatel_group_patents,
    COUNTIF(has_lucent) AS lucent_patents,
    COUNTIF(has_alcatel_group OR has_lucent) AS alcatel_lucent_union,
    COUNTIF(has_alcatel_group AND has_lucent) AS overlap_double_counted,
    ROUND(COUNTIF(has_alcatel_group OR has_lucent) / COUNT(*) * 100, 1) AS alcatel_lucent_share_pct
FROM per_patent;
