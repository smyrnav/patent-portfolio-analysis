-- Checks whether filtering on kind code B dropped older US patents.
SELECT
  SUBSTR(p.kind_code, 1, 1) AS kind,
  COUNT(DISTINCT p.publication_number) AS patents,
  MIN(p.grant_date) AS first_grant,
  MAX(p.grant_date) AS last_grant
FROM `patents-public-data.patents.publications` AS p,
  UNNEST(p.assignee_harmonized) AS a
WHERE p.country_code = 'US'
  AND p.grant_date > 0
  AND REGEXP_CONTAINS(
    UPPER(a.name),
    r'\bNOKIA\b|\bALCATEL\b|\bLUCENT TECHNOLOGIES\b|\bINFINERA\b'
  )
GROUP BY kind
ORDER BY patents DESC;
