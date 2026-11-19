-- Widen the ICEYE net: every distinct harmonized assignee name containing
-- "iceye" in the worldwide publications table, with family counts.
-- Purpose: the pool census found only 6 ICEYE families; check for name
-- variants (Oy, Ltd, Inc, subsidiaries, misspellings) before concluding
-- their patent record is tiny.
SELECT
  a.name AS assignee_name,
  COUNT(DISTINCT p.family_id) AS families,
  COUNT(DISTINCT p.publication_number) AS publications,
  MIN(p.filing_date) AS earliest,
  MAX(p.filing_date) AS latest
FROM `patents-public-data.patents.publications` AS p,
  UNNEST(p.assignee_harmonized) AS a
WHERE UPPER(a.name) LIKE '%ICEYE%'
GROUP BY assignee_name
ORDER BY families DESC;
