-- Does SpaceX patent? Name census for SpaceX/Starlink.
-- Answer (10 Nov 2026): SPACE EXPLORATION TECH CORP has 366 publications /
-- 110 families — about 175x fewer than Airbus, 7x fewer than Viasat.
-- A trade-secret strategy, not a technology gap; recorded in
-- docs/01-research-design/satcom-code-pools.md (known risks).
SELECT
  a.name,
  a.country_code,
  COUNT(*) AS pubs,
  COUNT(DISTINCT p.family_id) AS families
FROM `patents-public-data.patents.publications` AS p, UNNEST(p.assignee_harmonized) AS a
WHERE REGEXP_CONTAINS(UPPER(a.name), r'SPACEX|SPACE EXPLORATION TECH|STARLINK')
GROUP BY a.name, a.country_code
ORDER BY pubs DESC
LIMIT 30;
