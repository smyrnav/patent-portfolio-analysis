-- Superseded by 05_owner_names_all_years.sql: the kind code filter below misses US patents granted before 2001.
-- Owner names for companies absorbed through deals, left out of the first query.
-- \b matches whole words, so TRANSLUCENT is excluded. Alcatel names are already in query 01.
SELECT
  a.name AS owner,
  COUNT(DISTINCT p.publication_number) AS granted_patents
FROM `patents-public-data.patents.publications` AS p,
  UNNEST(p.assignee_harmonized) AS a
WHERE p.country_code = 'US'
  AND p.grant_date > 0
  AND p.kind_code LIKE 'B%'
  AND REGEXP_CONTAINS(UPPER(a.name), r'\b(LUCENT|BELL LABS|INFINERA)\b')
  AND NOT REGEXP_CONTAINS(UPPER(a.name), r'ALCATEL')
GROUP BY owner
ORDER BY granted_patents DESC;
