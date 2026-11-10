-- Satcom-pool patents filed at the Ukrainian patent office, any owner (discovery query).
-- Which companies consider the Ukrainian market worth protecting satcom technology in?
-- Same CPC prefixes as 25_ukraine_satcom_assignees.sql.
SELECT
  a.name,
  a.country_code AS assignee_country,
  COUNT(DISTINCT p.publication_number) AS ua_filings,
  COUNT(DISTINCT p.family_id) AS families
FROM `patents-public-data.patents.publications` AS p, UNNEST(p.assignee_harmonized) AS a
WHERE p.country_code = 'UA'
  AND EXISTS (
    SELECT 1 FROM UNNEST(p.cpc) AS c
    WHERE STARTS_WITH(c.code, 'H04B7/185')
       OR STARTS_WITH(c.code, 'H04B7/195')
       OR STARTS_WITH(c.code, 'H04B10/118')
       OR STARTS_WITH(c.code, 'H04W84/06')
       OR STARTS_WITH(c.code, 'H04K1/')
       OR STARTS_WITH(c.code, 'H04K3/')
  )
GROUP BY a.name, assignee_country
ORDER BY ua_filings DESC
LIMIT 200
