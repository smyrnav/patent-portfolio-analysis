-- Pool census (validation stage 0): families per satcom pool x owner x period.
-- Nokia lineage from portfolio_30y, the five actors from satcom_peers_30y.
-- PRE-VALIDATION discovery counts: the pools are candidates, so these numbers
-- describe what the code prefixes catch, not yet validated capabilities.
-- Pool rules from docs/01-research-design/satcom-code-pools.md.
-- Prefix note: H04B7/1851 (SAT) also prefixes 7/18517 (GRD earth stations),
-- so SAT excludes the 7/18517 branch explicitly.
WITH tagged AS (
  SELECT family_id, 'Nokia (lineage)' AS owner, cpc_codes, priority_date
  FROM nokia_analytics.portfolio_30y
  UNION ALL
  SELECT p.family_id, o AS owner, p.cpc_codes, p.priority_date
  FROM nokia_analytics.satcom_peers_30y AS p, UNNEST(p.owners) AS o
),
memberships AS (
  SELECT family_id, owner, 'SAT' AS pool, priority_date FROM tagged
  WHERE EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c
                WHERE STARTS_WITH(c, 'H04B7/195')
                   OR (STARTS_WITH(c, 'H04B7/1851') AND NOT STARTS_WITH(c, 'H04B7/18517')))
  UNION ALL
  SELECT family_id, owner, 'ISL', priority_date FROM tagged
  WHERE EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c
                WHERE STARTS_WITH(c, 'H04B7/18521') OR STARTS_WITH(c, 'H04B10/118'))
  UNION ALL
  SELECT family_id, owner, 'GRD', priority_date FROM tagged
  WHERE EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c
                WHERE STARTS_WITH(c, 'H04B7/18517') OR STARTS_WITH(c, 'H04B7/18528'))
  UNION ALL
  SELECT family_id, owner, 'NET', priority_date FROM tagged
  WHERE EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c
                WHERE STARTS_WITH(c, 'H04W84/06') OR STARTS_WITH(c, 'H04B7/18584')
                   OR STARTS_WITH(c, 'H04B7/18541'))
  UNION ALL
  SELECT family_id, owner, 'SEC', priority_date FROM tagged
  -- R1 (11 Nov 2026): SEC is a co-occurrence rule — at least one satellite
  -- prefix AND at least one security prefix on the same family.
  -- Corrected 24 November 2026: this branch previously tagged SEC from the
  -- security/watch codes alone, which contradicts the codebook; the saved
  -- pool_census.csv SEC counts were produced under that inconsistent rule.
  WHERE EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c
                WHERE STARTS_WITH(c, 'H04B7/195') OR STARTS_WITH(c, 'H04B7/1851')
                   OR STARTS_WITH(c, 'H04B7/18521') OR STARTS_WITH(c, 'H04B10/118')
                   OR STARTS_WITH(c, 'H04B7/18528')
                   OR STARTS_WITH(c, 'H04W84/06') OR STARTS_WITH(c, 'H04B7/18584')
                   OR STARTS_WITH(c, 'H04B7/18541'))
    AND EXISTS (SELECT 1 FROM UNNEST(cpc_codes) AS c
                WHERE STARTS_WITH(c, 'H04K1/') OR STARTS_WITH(c, 'H04K3/'))
  -- Watch items (not part of the rule): satellite-specific access codes
  -- H04B 7/18565 and 7/18593 are too rare to sample (codebook v2.0).
)
SELECT
  owner,
  pool,
  CASE
    WHEN priority_date >= 20200101 THEN '2020s'
    WHEN priority_date >= 20100101 THEN '2010s'
    WHEN priority_date >= 20000101 THEN '2000s'
    ELSE 'pre-2000'
  END AS period,
  COUNT(DISTINCT family_id) AS families
FROM memberships
GROUP BY owner, pool, period
ORDER BY owner, pool, period;
