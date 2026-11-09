-- Name census for the sovereign-satcom actors (question log Q24).
-- Broad patterns first, reviewed by eye afterwards — the same procedure as 01 and 02.
-- Deliberately no technology, office or grant filter: those choices belong to the peers table build.
-- One scan; a name matching two patterns lands in the first matching group, which the review will catch.
SELECT
  CASE
    WHEN UPPER(a.name) LIKE '%ICEYE%' THEN 'ICEYE'
    WHEN UPPER(a.name) LIKE '%EUTELSAT%' OR UPPER(a.name) LIKE '%ONEWEB%'
      OR UPPER(a.name) LIKE '%ONE WEB%' OR UPPER(a.name) LIKE '%WORLDVU%' THEN 'Eutelsat/OneWeb'
    WHEN UPPER(a.name) LIKE '%VIASAT%' OR UPPER(a.name) LIKE '%VIA SAT%'
      OR UPPER(a.name) LIKE '%INMARSAT%' THEN 'Viasat'
    WHEN UPPER(a.name) LIKE '%THALES%' OR UPPER(a.name) LIKE '%ALENIA%' THEN 'Thales Alenia Space'
    WHEN UPPER(a.name) LIKE '%AIRBUS%' OR UPPER(a.name) LIKE '%ASTRIUM%'
      OR UPPER(a.name) LIKE '%EADS%' THEN 'Airbus Defence and Space'
  END AS actor,
  a.name AS name,
  COUNT(DISTINCT p.publication_number) AS publications
FROM `patents-public-data.patents.publications` AS p,
  UNNEST(p.assignee_harmonized) AS a
WHERE REGEXP_CONTAINS(UPPER(a.name), r'ICEYE|EUTELSAT|ONEWEB|ONE WEB|WORLDVU|VIASAT|VIA SAT|INMARSAT|THALES|ALENIA|AIRBUS|ASTRIUM|EADS')
GROUP BY actor, name
ORDER BY actor, publications DESC;
