-- Superseded by 05_owner_names_all_years.sql: the kind code filter below misses US patents granted before 2001.
-- Every owner name attached to granted US patents that mentions Nokia or Alcatel.
SELECT
  a.name AS owner,
  COUNT(DISTINCT p.publication_number) AS granted_patents
FROM `patents-public-data.patents.publications` AS p,
  UNNEST(p.assignee_harmonized) AS a
WHERE p.country_code = 'US'
  AND p.grant_date > 0
  AND p.kind_code LIKE 'B%'
  AND (UPPER(a.name) LIKE '%NOKIA%' OR UPPER(a.name) LIKE '%ALCATEL%')
GROUP BY owner
ORDER BY granted_patents DESC;
