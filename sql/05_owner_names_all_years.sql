-- Replaces queries 01 and 02. Kind A covers older US patents, B newer ones and E reissues.
-- Design patents (S) and invention registrations (H) are left out.
-- The search is deliberately broad, and src/clean_owner_names.py removes false matches.
SELECT
  a.name AS owner,
  COUNT(DISTINCT p.publication_number) AS granted_patents,
  MIN(p.grant_date) AS first_grant,
  MAX(p.grant_date) AS last_grant
FROM `patents-public-data.patents.publications` AS p,
  UNNEST(p.assignee_harmonized) AS a
WHERE p.country_code = 'US'
  AND p.grant_date > 0
  AND SUBSTR(p.kind_code, 1, 1) IN ('A', 'B', 'E')
  AND REGEXP_CONTAINS(UPPER(a.name), r'NOKIA|ALCATEL|\bLUCENT\b|BELL LABS|INFINERA')
GROUP BY owner
ORDER BY granted_patents DESC;
