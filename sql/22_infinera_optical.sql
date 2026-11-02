-- Infinera split for H1: US-granted families (filed since Nov 2006) with at least one
-- Infinera owner name, against the optical retrieval pool (H04B10/H04J14/H04Q11/00).
-- Pool membership is not a validated optical label; apply the Nokia OPT precision factor
-- from data/validation/results_precision.csv before quoting a class estimate.
WITH fam AS (
    SELECT family_id,
        MAX(EXISTS (SELECT 1 FROM UNNEST(owners) AS o WHERE UPPER(o) LIKE '%INFINERA%')) AS infinera,
        MAX(EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c WHERE REGEXP_CONTAINS(c, r'^(H04B10/|H04J14/|H04Q11/00)'))) AS optical_pool,
        MIN(priority_date) AS first_priority
    FROM nokia_analytics.portfolio_30y
    WHERE country_code = 'US' AND grant_date > 0 AND filing_date >= 20061101 AND STARTS_WITH(kind_code, 'B')
    GROUP BY family_id
)
SELECT
    infinera,
    COUNT(*) AS families,
    COUNTIF(optical_pool) AS optical_pool_families,
    COUNTIF(optical_pool AND first_priority >= 20160101) AS optical_pool_since_2016
FROM fam
GROUP BY infinera
ORDER BY infinera DESC;
