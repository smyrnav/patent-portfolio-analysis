-- Re-test sample (validation stage 3): 150 families from the COMBINED satcom pool,
-- excluding pilot families, stratified by owner and priority period (largest
-- remainder), deterministic ordering. Amended pool rules (pilot decisions R1-R5):
-- SEC is a co-occurrence of a satellite prefix and a security prefix; ISL is a
-- flag, not a bucket; the combined pool is the primary measure (R2).
-- Each row is tagged with every pool that caught the family, so per-pool
-- precision can be reported as tentative alongside the combined score.
-- Representative publication per family: US/WO/EP/GB members only, so the
-- numbered sentences and the description paragraph are readable in English.
WITH pilot_fams AS (
  SELECT f FROM UNNEST(['22116304', '22265101', '24421036', '32241536', '35732965', '35976498', '36203937', '36907535', '37496653', '37896100', '37898773', '38024333', '38175805', '38645792', '39344974', '39535615', '39863143', '40523687', '41327307', '42061116', '42315215', '42543158', '42936632', '43012750', '43014389', '43066988', '43242267', '45908008', '46514053', '47019047', '47880592', '48040272', '48041750', '48050405', '48128340', '48170377', '48430724', '49231547', '49261986', '49322424', '50188190', '50490830', '50624629', '50774792', '50981434', '51014315', '51225675', '51841662', '51895869', '53489873', '53758254', '54365307', '54937119', '56084078', '56101519', '57130138', '58669925', '59974484', '60263075', '60923523', '60941388', '60941523', '61070080', '61655809', '61899136', '62872778', '65685385', '67107743', '67185094', '67539998', '67777298', '68136376', '68848467', '68916438', '69104554', '70804735', '74045645', '75336686', '75529845', '75529913', '75914377', '76444250', '77822005', '78828027', '79170947', '80595448', '80953513', '81207745', '82156553', '82404240', '8242043', '83154876', '83396388', '83998930', '84103337', '84359286', '84360452', '84360690', '8492752', '85076418', '85227343', '85382541', '85685209', '85796765', '85936990', '86007302', '86099872', '86386852', '86657573', '86657755', '87426610', '87553528', '87760525', '8866028', '88690050', '88863380', '89158550', '89663323', '89834167', '89900757', '90368166', '90789527', '90829228', '90880579', '90928548', '91738509', '92051190', '92538674', '93037220', '94331364', '94481446', '94581875', '94928051', '9493146', '95064224', '95519178', '95699923', '95745588', '95745667', '96026918', '96496606', '96917640', '97067504', '97229797', '97591539', '98520886', '98654562']) AS f
),
tagged AS (
  SELECT family_id, 'Nokia (lineage)' AS owner, publication_number, country_code,
         kind_code, cpc_codes, priority_date, title_en
  FROM nokia_analytics.portfolio_30y
  UNION ALL
  SELECT p.family_id, o AS owner, p.publication_number, p.country_code,
         p.kind_code, p.cpc_codes, p.priority_date, p.title_en
  FROM nokia_analytics.satcom_peers_30y AS p, UNNEST(p.owners) AS o
),
codes AS (
  SELECT family_id, owner, cpc_codes FROM tagged GROUP BY family_id, owner, cpc_codes
),
matched AS (
  SELECT DISTINCT family_id, owner, c
  FROM codes, UNNEST(cpc_codes) AS c
  WHERE STARTS_WITH(c, 'H04B7/195')
     OR (STARTS_WITH(c, 'H04B7/1851') AND NOT STARTS_WITH(c, 'H04B7/18517'))
     OR STARTS_WITH(c, 'H04B7/18521') OR STARTS_WITH(c, 'H04B10/118')
     OR STARTS_WITH(c, 'H04B7/18517') OR STARTS_WITH(c, 'H04B7/18528')
     OR STARTS_WITH(c, 'H04W84/06') OR STARTS_WITH(c, 'H04B7/18584')
     OR STARTS_WITH(c, 'H04B7/18541') OR STARTS_WITH(c, 'H04K1/') OR STARTS_WITH(c, 'H04K3/')
),
flags AS (
  SELECT
    family_id,
    owner,
    MAX(CASE WHEN STARTS_WITH(c, 'H04B7/195')
      OR (STARTS_WITH(c, 'H04B7/1851') AND NOT STARTS_WITH(c, 'H04B7/18517'))
      THEN 1 ELSE 0 END) AS has_sat,
    MAX(CASE WHEN STARTS_WITH(c, 'H04B7/18521') OR STARTS_WITH(c, 'H04B10/118') THEN 1 ELSE 0 END) AS has_isl,
    MAX(CASE WHEN STARTS_WITH(c, 'H04B7/18517') OR STARTS_WITH(c, 'H04B7/18528') THEN 1 ELSE 0 END) AS has_grd,
    MAX(CASE WHEN STARTS_WITH(c, 'H04W84/06') OR STARTS_WITH(c, 'H04B7/18584')
      OR STARTS_WITH(c, 'H04B7/18541') THEN 1 ELSE 0 END) AS has_net,
    MAX(CASE WHEN STARTS_WITH(c, 'H04K1/') OR STARTS_WITH(c, 'H04K3/') THEN 1 ELSE 0 END) AS has_sec_code,
    STRING_AGG(c ORDER BY c) AS matched_codes
  FROM matched
  GROUP BY family_id, owner
),
pool_fams AS (
  SELECT
    f.family_id, f.owner, f.matched_codes,
    (f.has_sat = 1 OR f.has_isl = 1 OR f.has_grd = 1 OR f.has_net = 1) AS any_satellite,
    TRIM(CONCAT(
      IF(f.has_sat = 1, 'SAT,', ''), IF(f.has_isl = 1, 'ISL,', ''),
      IF(f.has_grd = 1, 'GRD,', ''), IF(f.has_net = 1, 'NET,', ''),
      IF(f.has_sec_code = 1 AND (f.has_sat = 1 OR f.has_isl = 1 OR f.has_grd = 1 OR f.has_net = 1), 'SEC', '')
    ), ',') AS pools_matched
  FROM flags AS f
),
eligible AS (
  SELECT p.*, t.priority_date
  FROM pool_fams AS p
  JOIN (SELECT family_id, owner, MIN(priority_date) AS priority_date FROM tagged GROUP BY family_id, owner) AS t
    ON t.family_id = p.family_id AND t.owner = p.owner
  JOIN (SELECT DISTINCT family_id, owner FROM tagged WHERE country_code IN ('US', 'WO', 'EP', 'GB')) AS e
    ON e.family_id = p.family_id AND e.owner = p.owner
  LEFT JOIN pilot_fams ON pilot_fams.f = p.family_id
  WHERE p.any_satellite AND pilot_fams.f IS NULL
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
base AS (
  SELECT
    e.family_id, e.owner, e.pools_matched, e.matched_codes, e.priority_date,
    CASE
      WHEN e.priority_date >= 20200101 THEN '2020s'
      WHEN e.priority_date >= 20100101 THEN '2010s'
      WHEN e.priority_date >= 20000101 THEN '2000s'
      ELSE 'pre-2000'
    END AS period,
    r.publication_number, r.title_en,
    r.cpc_codes[SAFE_OFFSET(0)] AS first_code
  FROM eligible AS e
  JOIN reps AS r ON r.family_id = e.family_id AND r.owner = e.owner
),
owner_avail AS (
  SELECT owner, COUNT(*) AS avail FROM base GROUP BY owner
),
owner_share AS (
  SELECT owner, avail, 150.0 * avail / SUM(avail) OVER () AS share FROM owner_avail
),
owner_base AS (
  SELECT owner, avail, LEAST(CAST(FLOOR(share) AS INT64), avail) AS base_q,
         share - FLOOR(share) AS frac
  FROM owner_share
),
owner_quota AS (
  SELECT b.owner,
    b.base_q + IF(b.base_q < b.avail AND r.rn <= 150 - s.assigned, 1, 0) AS quota
  FROM owner_base AS b
  CROSS JOIN (SELECT SUM(base_q) AS assigned FROM owner_base) AS s
  LEFT JOIN (
    SELECT owner, ROW_NUMBER() OVER (ORDER BY frac DESC, owner) AS rn
    FROM owner_base WHERE base_q < avail
  ) AS r ON r.owner = b.owner
),
period_avail AS (
  SELECT owner, period, COUNT(*) AS avail FROM base GROUP BY owner, period
),
period_share AS (
  SELECT p.owner, p.period, p.avail, q.quota,
    q.quota * p.avail / SUM(p.avail) OVER (PARTITION BY p.owner) AS share
  FROM period_avail AS p
  JOIN owner_quota AS q ON q.owner = p.owner
),
period_base AS (
  SELECT owner, period, avail, quota,
    LEAST(CAST(FLOOR(share) AS INT64), avail) AS base_q,
    share - FLOOR(share) AS frac
  FROM period_share
),
period_quota AS (
  SELECT b.owner, b.period,
    b.base_q + IF(b.base_q < b.avail AND r.rn <= b.quota - s.assigned, 1, 0) AS quota
  FROM period_base AS b
  CROSS JOIN (SELECT owner, SUM(base_q) AS assigned FROM period_base GROUP BY owner) AS s
  LEFT JOIN (
    SELECT owner, period, ROW_NUMBER() OVER (PARTITION BY owner ORDER BY frac DESC, period) AS rn
    FROM period_base WHERE base_q < avail
  ) AS r ON r.owner = b.owner AND r.period = b.period
  WHERE s.owner = b.owner
),
numbered AS (
  SELECT b.*, q.quota,
    ROW_NUMBER() OVER (
      PARTITION BY b.owner, b.period
      ORDER BY FARM_FINGERPRINT(CONCAT(CAST(b.family_id AS STRING), '|combined|satcom-retest'))
    ) AS rn
  FROM base AS b
  JOIN period_quota AS q ON q.owner = b.owner AND q.period = b.period
)
SELECT
  'satcom-retest' AS stage,
  'COMBINED' AS pool,
  owner AS company,
  publication_number,
  family_id,
  priority_date,
  period,
  pools_matched,
  matched_codes,
  first_code,
  title_en
FROM numbered
WHERE rn <= quota
ORDER BY company, period, publication_number;
