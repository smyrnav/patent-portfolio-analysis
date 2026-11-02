-- Raw retrieval-pool family counts by company and priority period, for H2.
-- Same company attribution and filters as 16_codebook_sample.sql (US granted members since Nov 2006).
-- These are POOL counts, not validated class counts: multiply by the per-company precision
-- factors in data/validation/results_precision.csv before comparing, and report the 95% ranges.
-- A family can sit in more than one pool; that is intended.
WITH b AS (
    SELECT 'Nokia' AS co, family_id, cpc_codes, priority_date
    FROM nokia_analytics.portfolio_30y
    WHERE country_code = 'US' AND grant_date > 0 AND filing_date >= 20061101 AND STARTS_WITH(kind_code, 'B')
    UNION ALL
    SELECT CASE
        WHEN REGEXP_CONTAINS(UPPER(ARRAY_TO_STRING(owners, ' ')), r'CIENA') THEN 'Ciena'
        WHEN REGEXP_CONTAINS(UPPER(ARRAY_TO_STRING(owners, ' ')), r'CISCO|ACACIA|LUXTERA') THEN 'Cisco'
        WHEN REGEXP_CONTAINS(UPPER(ARRAY_TO_STRING(owners, ' ')), r'ARISTA') THEN 'Arista'
        WHEN REGEXP_CONTAINS(UPPER(ARRAY_TO_STRING(owners, ' ')), r'HUAWEI') THEN 'Huawei'
        ELSE 'Other'
    END, family_id, cpc_codes, priority_date
    FROM nokia_analytics.rivals_30y
    WHERE country_code = 'US' AND grant_date > 0 AND filing_date >= 20061101 AND STARTS_WITH(kind_code, 'B')
), fam AS (
    SELECT co, family_id, MIN(priority_date) AS first_priority,
        MAX(EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c WHERE REGEXP_CONTAINS(c, r'^(H04B10/|H04J14/|H04Q11/00)'))) AS opt,
        MAX(EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c WHERE STARTS_WITH(c, 'H04L45/'))) AS ipr,
        MAX(EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c WHERE STARTS_WITH(c, 'H04L49/'))) AS dcs
    FROM b
    WHERE co != 'Other'
    GROUP BY co, family_id
), labelled AS (
    SELECT co, family_id,
        CASE
            WHEN first_priority <= 20101231 THEN 'to 2010'
            WHEN first_priority <= 20151231 THEN '2011-2015'
            WHEN first_priority <= 20201231 THEN '2016-2020'
            ELSE '2021 on'
        END AS period,
        opt, ipr, dcs
    FROM fam
)
SELECT pool, co, period, COUNT(*) AS pool_families
FROM labelled, UNNEST(['OPT', 'IPR', 'DCS']) AS pool
WHERE (pool = 'OPT' AND opt) OR (pool = 'IPR' AND ipr) OR (pool = 'DCS' AND dcs)
GROUP BY pool, co, period
ORDER BY pool, co, period;
