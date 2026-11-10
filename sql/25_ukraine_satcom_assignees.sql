-- Ukrainian assignees holding satcom-pool patents (discovery query).
-- Who inside Ukraine holds patents relevant to a sovereign satcom system?
-- CPC prefixes come from the candidate pools in docs/01-research-design/satcom-code-pools.md
-- (broadened to prefix level; this is discovery, not the validated pool census).
SELECT
  a.name,
  COUNT(DISTINCT p.publication_number) AS publications,
  COUNT(DISTINCT p.family_id) AS families
FROM `patents-public-data.patents.publications` AS p, UNNEST(p.assignee_harmonized) AS a
WHERE a.country_code = 'UA'
  AND EXISTS (
    SELECT 1 FROM UNNEST(p.cpc) AS c
    WHERE STARTS_WITH(c.code, 'H04B7/185')
       OR STARTS_WITH(c.code, 'H04B7/195')
       OR STARTS_WITH(c.code, 'H04B10/118')
       OR STARTS_WITH(c.code, 'H04W84/06')
       OR STARTS_WITH(c.code, 'H04K1/')
       OR STARTS_WITH(c.code, 'H04K3/')
  )
GROUP BY a.name
ORDER BY families DESC, publications DESC
