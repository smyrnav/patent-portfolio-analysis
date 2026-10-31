-- US patents filed in the last 30 years, by owner name and filing year.
-- Filing date is used because a US patent generally lasts 20 years from filing.
-- False matches are removed afterwards. Save the results as CSV.
SELECT
  a.name AS owner,
  CAST(FLOOR(p.filing_date / 10000) AS INT64) AS filing_year,
  COUNT(DISTINCT p.publication_number) AS granted_patents
FROM `patents-public-data.patents.publications` AS p,
  UNNEST(p.assignee_harmonized) AS a
WHERE p.country_code = 'US'
  AND p.grant_date > 0
  AND p.filing_date >= 19961101
  AND SUBSTR(p.kind_code, 1, 1) IN ('A', 'B', 'E')
  AND REGEXP_CONTAINS(UPPER(a.name), r'NOKIA|ALCATEL|\bLUCENT\b|INFINERA')
GROUP BY owner, filing_year
ORDER BY owner, filing_year;
