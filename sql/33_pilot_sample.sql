-- Pilot sample (validation stage 1): 30 families per satcom pool, 150 total.
-- Stratified: proportional allocation across the six owners, then across
-- priority periods inside each owner cell (largest remainder both times).
-- Deterministic: FARM_FINGERPRINT ordering, no RAND().
-- One representative publication per family, restricted to US/WO/EP/GB members
-- so the numbered sentences at the back are readable in English.
-- matched_codes lists every pool prefix that caught the family, so precision
-- can later be reported per code, not only per pool.
-- first_code is the first CPC entry in the representative publication's array,
-- used as a proxy for listing order (the array does not document its order).
WITH tagged AS (
  SELECT family_id, 'Nokia (lineage)' AS owner, publication_number, country_code,
         kind_code, cpc_codes, priority_date, title_en
  FROM nokia_analytics.portfolio_30y
  UNION ALL
  SELECT p.family_id, o AS owner, p.publication_number, p.country_code,
         p.kind_code, p.cpc_codes, p.priority_date, p.title_en
  FROM nokia_analytics.satcom_peers_30y AS p, UNNEST(p.owners) AS o
),
memberships AS (
  SELECT family_id, owner, 'SAT' AS pool, c AS matched_code FROM tagged, UNNEST(cpc_codes) AS c
  WHERE STARTS_WITH(c, 'H04B7/195')
     OR (STARTS_WITH(c, 'H04B7/1851') AND NOT STARTS_WITH(c, 'H04B7/18517'))
  UNION ALL
  SELECT family_id, owner, 'ISL', c FROM tagged, UNNEST(cpc_codes) AS c
  WHERE STARTS_WITH(c, 'H04B7/18521') OR STARTS_WITH(c, 'H04B10/118')
  UNION ALL
  SELECT family_id, owner, 'GRD', c FROM tagged, UNNEST(cpc_codes) AS c
  WHERE STARTS_WITH(c, 'H04B7/18517') OR STARTS_WITH(c, 'H04B7/18528')
  UNION ALL
  SELECT family_id, owner, 'NET', c FROM tagged, UNNEST(cpc_codes) AS c
  WHERE STARTS_WITH(c, 'H04W84/06') OR STARTS_WITH(c, 'H04B7/18584')
     OR STARTS_WITH(c, 'H04B7/18541')
  UNION ALL
  SELECT family_id, owner, 'SEC', c FROM tagged, UNNEST(cpc_codes) AS c
  WHERE STARTS_WITH(c, 'H04K1/') OR STARTS_WITH(c, 'H04K3/')
     OR STARTS_WITH(c, 'H04B7/18565') OR STARTS_WITH(c, 'H04B7/18593')
),
fams AS (
  SELECT
    m.family_id,
    m.owner,
    m.pool,
    STRING_AGG(DISTINCT m.matched_code ORDER BY m.matched_code) AS matched_codes,
    MIN(t.priority_date) AS priority_date
  FROM memberships AS m
  JOIN (
    SELECT family_id, owner, MIN(priority_date) AS priority_date
    FROM tagged
    GROUP BY family_id, owner
  ) AS t
    ON t.family_id = m.family_id AND t.owner = m.owner
  JOIN (
    SELECT DISTINCT family_id, owner
    FROM tagged
    WHERE country_code IN ('US', 'WO', 'EP', 'GB')
  ) AS e
    ON e.family_id = m.family_id AND e.owner = m.owner
  GROUP BY m.family_id, m.owner, m.pool
),
reps AS (
  SELECT family_id, owner, publication_number, title_en, cpc_codes
  FROM (
    SELECT t.*,
      ROW_NUMBER() OVER (
        PARTITION BY t.family_id, t.owner
        ORDER BY CASE
          WHEN t.country_code = 'US' AND STARTS_WITH(t.kind_code, 'B') THEN 1
          WHEN t.country_code = 'US' THEN 2
          WHEN t.country_code = 'WO' THEN 3
          WHEN t.country_code = 'EP' THEN 4
          ELSE 5
        END, t.publication_number
      ) AS pick
    FROM tagged AS t
    WHERE t.country_code IN ('US', 'WO', 'EP', 'GB')
  )
  WHERE pick = 1
),
pool_fams AS (
  SELECT
    f.family_id, f.owner, f.pool, f.matched_codes, f.priority_date,
    CASE
      WHEN f.priority_date >= 20200101 THEN '2020s'
      WHEN f.priority_date >= 20100101 THEN '2010s'
      WHEN f.priority_date >= 20000101 THEN '2000s'
      ELSE 'pre-2000'
    END AS period,
    r.publication_number, r.title_en,
    r.cpc_codes[SAFE_OFFSET(0)] AS first_code
  FROM fams AS f
  JOIN reps AS r ON r.family_id = f.family_id AND r.owner = f.owner
),
owner_avail AS (
  SELECT pool, owner, COUNT(*) AS avail
  FROM pool_fams
  GROUP BY pool, owner
),
owner_share AS (
  SELECT
    pool, owner, avail,
    30.0 * avail / SUM(avail) OVER (PARTITION BY pool) AS share
  FROM owner_avail
),
owner_base AS (
  SELECT
    pool, owner, avail,
    LEAST(CAST(FLOOR(share) AS INT64), avail) AS base,
    share - FLOOR(share) AS frac
  FROM owner_share
),
owner_quota AS (
  SELECT
    b.pool, b.owner,
    b.base + IF(b.base < b.avail AND r.rn <= 30 - s.assigned, 1, 0) AS quota
  FROM owner_base AS b
  CROSS JOIN (SELECT pool, SUM(base) AS assigned FROM owner_base GROUP BY pool) AS s
  LEFT JOIN (
    SELECT pool, owner,
      ROW_NUMBER() OVER (PARTITION BY pool ORDER BY frac DESC, owner) AS rn
    FROM owner_base
    WHERE base < avail
  ) AS r ON r.pool = b.pool AND r.owner = b.owner
  WHERE s.pool = b.pool
),
period_avail AS (
  SELECT pool, owner, period, COUNT(*) AS avail
  FROM pool_fams
  GROUP BY pool, owner, period
),
period_share AS (
  SELECT
    p.pool, p.owner, p.period, p.avail,
    q.quota * p.avail / SUM(p.avail) OVER (PARTITION BY p.pool, p.owner) AS share,
    q.quota
  FROM period_avail AS p
  JOIN owner_quota AS q ON q.pool = p.pool AND q.owner = p.owner
),
period_base AS (
  SELECT
    pool, owner, period, avail, quota,
    LEAST(CAST(FLOOR(share) AS INT64), avail) AS base,
    share - FLOOR(share) AS frac
  FROM period_share
),
period_quota AS (
  SELECT
    b.pool, b.owner, b.period,
    b.base + IF(b.base < b.avail AND r.rn <= b.quota - s.assigned, 1, 0) AS quota
  FROM period_base AS b
  CROSS JOIN (
    SELECT pool, owner, SUM(base) AS assigned
    FROM period_base GROUP BY pool, owner
  ) AS s
  LEFT JOIN (
    SELECT pool, owner, period,
      ROW_NUMBER() OVER (PARTITION BY pool, owner ORDER BY frac DESC, period) AS rn
    FROM period_base
    WHERE base < avail
  ) AS r ON r.pool = b.pool AND r.owner = b.owner AND r.period = b.period
  WHERE s.pool = b.pool AND s.owner = b.owner
),
numbered AS (
  SELECT
    f.*,
    q.quota,
    ROW_NUMBER() OVER (
      PARTITION BY f.pool, f.owner, f.period
      ORDER BY FARM_FINGERPRINT(CONCAT(CAST(f.family_id AS STRING), '|', f.pool, '|satcom-pilot'))
    ) AS rn
  FROM pool_fams AS f
  JOIN period_quota AS q ON q.pool = f.pool AND q.owner = f.owner AND q.period = f.period
)
SELECT
  'satcom-pilot' AS stage,
  pool,
  owner AS company,
  publication_number,
  family_id,
  priority_date,
  period,
  matched_codes,
  first_code,
  CASE
    WHEN pool = 'SAT' THEN STARTS_WITH(first_code, 'H04B7/195')
      OR (STARTS_WITH(first_code, 'H04B7/1851') AND NOT STARTS_WITH(first_code, 'H04B7/18517'))
    WHEN pool = 'ISL' THEN STARTS_WITH(first_code, 'H04B7/18521') OR STARTS_WITH(first_code, 'H04B10/118')
    WHEN pool = 'GRD' THEN STARTS_WITH(first_code, 'H04B7/18517') OR STARTS_WITH(first_code, 'H04B7/18528')
    WHEN pool = 'NET' THEN STARTS_WITH(first_code, 'H04W84/06') OR STARTS_WITH(first_code, 'H04B7/18584')
      OR STARTS_WITH(first_code, 'H04B7/18541')
    WHEN pool = 'SEC' THEN STARTS_WITH(first_code, 'H04K1/') OR STARTS_WITH(first_code, 'H04K3/')
      OR STARTS_WITH(first_code, 'H04B7/18565') OR STARTS_WITH(first_code, 'H04B7/18593')
  END AS first_code_matches_pool,
  title_en
FROM numbered
WHERE rn <= quota
ORDER BY pool, company, period, publication_number;
