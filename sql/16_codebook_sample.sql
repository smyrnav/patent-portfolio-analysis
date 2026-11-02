-- Sampling limits exceed the final company slot quotas to provide spares for replacements.
-- Saved sample CSVs predate the explicit Huawei match and Other fallback; this edit does not regenerate them.
WITH b AS (
    SELECT 'Nokia' AS co, family_id, publication_number, cpc_codes
    FROM nokia_analytics.portfolio_30y
    WHERE country_code = 'US' AND grant_date > 0 AND filing_date >= 20061101 AND STARTS_WITH(kind_code, 'B')
    UNION ALL
    SELECT CASE
        WHEN REGEXP_CONTAINS(UPPER(ARRAY_TO_STRING(owners, ' ')), r'CIENA') THEN 'Ciena'
        WHEN REGEXP_CONTAINS(UPPER(ARRAY_TO_STRING(owners, ' ')), r'CISCO|ACACIA|LUXTERA') THEN 'Cisco'
        WHEN REGEXP_CONTAINS(UPPER(ARRAY_TO_STRING(owners, ' ')), r'ARISTA') THEN 'Arista'
        WHEN REGEXP_CONTAINS(UPPER(ARRAY_TO_STRING(owners, ' ')), r'HUAWEI') THEN 'Huawei'
        ELSE 'Other'
    END, family_id, publication_number, cpc_codes
    FROM nokia_analytics.rivals_30y
    WHERE country_code = 'US' AND grant_date > 0 AND filing_date >= 20061101 AND STARTS_WITH(kind_code, 'B')
), p AS (
    SELECT co, family_id, publication_number,
        CASE WHEN EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c WHERE REGEXP_CONTAINS(c, r'^(H04B10/|H04J14/|H04Q11/00)')) THEN 1 ELSE 0 END AS opt,
        CASE WHEN EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c WHERE STARTS_WITH(c, 'H04L45/')) THEN 1 ELSE 0 END AS ipr,
        CASE WHEN EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c WHERE REGEXP_CONTAINS(c, r'^(H04L49/|H04L47/)')) THEN 1 ELSE 0 END AS dcs
    FROM b
), l AS (
    SELECT 'OPT' AS pool, co, family_id, MIN(publication_number) AS pub FROM p WHERE opt = 1 GROUP BY co, family_id
    UNION ALL
    SELECT 'IPR', co, family_id, MIN(publication_number) FROM p WHERE ipr = 1 GROUP BY co, family_id
    UNION ALL
    SELECT 'DCS', co, family_id, MIN(publication_number) FROM p WHERE dcs = 1 GROUP BY co, family_id
), r AS (
    SELECT *, COUNT(*) OVER (PARTITION BY pool, co) AS pool_size,
        ROW_NUMBER() OVER (PARTITION BY pool, co ORDER BY FARM_FINGERPRINT(CONCAT('codebook-2026', family_id))) AS rn
    FROM l
)
SELECT pool, co, ANY_VALUE(pool_size) AS pool_size, STRING_AGG(pub, ' ' ORDER BY rn) AS sample
FROM r
WHERE rn <= CASE co WHEN 'Nokia' THEN 56 WHEN 'Huawei' THEN 17 WHEN 'Arista' THEN 17 ELSE 30 END
GROUP BY pool, co
ORDER BY pool, co;
