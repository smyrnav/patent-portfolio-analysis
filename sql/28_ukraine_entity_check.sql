-- Known-entity check: do Ukraine's space-industry names appear in the dataset
-- at all, and is there any large Ukrainian holder we missed?
-- Found ECHOSTAR UKRAINE LLC (114 publications, UA) — followed up in query 29.
-- No KB Pivdenne / Pivdenmash under these spellings; its heritage is rocket
-- platforms (B64G), outside the communications scope by design.
SELECT
  a.name,
  a.country_code,
  COUNT(*) AS pubs
FROM `patents-public-data.patents.publications` AS p, UNNEST(p.assignee_harmonized) AS a
WHERE REGEXP_CONTAINS(UPPER(a.name), r'PIVDEN|YUZH|HARTRON|KHARTRON|KB YUZH|UKRSAT|UKRAINE')
GROUP BY a.name, a.country_code
ORDER BY pubs DESC
LIMIT 50;
