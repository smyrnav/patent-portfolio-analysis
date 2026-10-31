-- Top technology areas per 5-year period, counted as inventions (patent families).
-- Each family is dated by its earliest filing in the table.
-- A family with several technology codes counts once in each area.
WITH families AS (
  SELECT family_id, MIN(filing_date) AS first_filing
  FROM nokia_analytics.portfolio_30y
  GROUP BY family_id
),
codes AS (
  SELECT DISTINCT p.family_id, SUBSTR(code, 1, 4) AS area
  FROM nokia_analytics.portfolio_30y AS p,
    UNNEST(p.cpc_codes) AS code
)
SELECT
  CAST(FLOOR((FLOOR(f.first_filing / 10000) - 1996) / 5) * 5 + 1996 AS INT64)
    AS period_start,
  c.area,
  COUNT(*) AS inventions
FROM families AS f
JOIN codes AS c USING (family_id)
GROUP BY period_start, c.area
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY period_start ORDER BY inventions DESC
) <= 8
ORDER BY period_start, inventions DESC;
