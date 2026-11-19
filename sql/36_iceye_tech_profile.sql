-- ICEYE technology profile: what do their ~60-70 families actually cover?
-- Family-level, deduplicated across the 9 known name variants (ICEYE OY,
-- ICEYE INC, ICEYE POLSKA misspellings), grouped by CPC class (first 4
-- characters). Answers Q: is ICEYE's small satcom-pool count (6 families)
-- a naming miss or a real feature of their portfolio?
WITH iceye_families AS (
  SELECT DISTINCT p.family_id
  FROM `patents-public-data.patents.publications` AS p,
    UNNEST(p.assignee_harmonized) AS a
  WHERE a.name IN (
    'ICEYE OY', 'ICEYE INC', 'ICEYE POLSKA SP Z O O',
    'ICEYE POLSKA SPOLKA Z OGRANICZONA ODPOWIEDZIALNOSCIA',
    'ICEYE POLSKA SPOLKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
    'ICEYE POLSKA SPOLKA Z ORGANIZONA ODPOWIEDZIALNOSCIA',
    'ICEYE POLSKA SPOLKA Z ORGRANIZONA ODPOWIEDZIALNOSCIA',
    'ICEYE POLSKA SPOLKA Z ORGRANIZONA ODPOWIEDZIALNOSCIA',
    'ICEYE POLSKA SPOTKA Z OGRANICZONA ODPOWIEDZIALNOSCIA'
  )
),
fam_codes AS (
  SELECT f.family_id, SUBSTR(c.code, 1, 4) AS cpc_class
  FROM iceye_families AS f
  JOIN `patents-public-data.patents.publications` AS p
    ON f.family_id = p.family_id,
  UNNEST(p.cpc) AS c
)
SELECT cpc_class, COUNT(DISTINCT family_id) AS families
FROM fam_codes
GROUP BY cpc_class
ORDER BY families DESC
LIMIT 25;
