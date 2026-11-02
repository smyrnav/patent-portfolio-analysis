-- Expiry curve for H3: families with grant evidence reaching the 20-year approximation each year.
-- Runs on nokia_analytics.family_status (built by 09_family_status.sql).
-- Limits: filing date + 20 years is an approximation (term adjustments, terminal disclaimers and
-- lapses are not visible here); core-owner names only; category split needs the validated
-- classifier applied to all families, which does not exist yet, so this is the overall curve.
SELECT
    CAST(SUBSTR(CAST(first_filing AS STRING), 1, 4) AS INT64) + 20 AS expiry_year,
    COUNT(*) AS families_reaching_20y,
    SUM(COUNT(*)) OVER (ORDER BY CAST(SUBSTR(CAST(first_filing AS STRING), 1, 4) AS INT64)) AS cumulative
FROM nokia_analytics.family_status
WHERE core_owner AND ever_granted
GROUP BY expiry_year
ORDER BY expiry_year;
