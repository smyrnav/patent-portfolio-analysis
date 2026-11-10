-- Follow-up to query 28: what does EchoStar's Ukrainian entity patent?
-- Answer: set-top-box video R&D (93 of 114 publications in H04N), not
-- satellite communications — correctly outside the satcom pools.
SELECT
  SUBSTR(c.code, 1, 4) AS cpc_class,
  COUNT(DISTINCT p.publication_number) AS pubs
FROM `patents-public-data.patents.publications` AS p,
     UNNEST(p.assignee_harmonized) AS a,
     UNNEST(p.cpc) AS c
WHERE a.name = 'ECHOSTAR UKRAINE LLC'
GROUP BY cpc_class
ORDER BY pubs DESC
LIMIT 10;
