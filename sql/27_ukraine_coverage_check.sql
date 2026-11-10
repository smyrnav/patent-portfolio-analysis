-- Coverage check behind query 25's empty Ukraine result: is the dataset's
-- Ukrainian coverage real, or is "no satcom patents" a data hole?
-- Answer (10 Nov 2026): 336,474 UA-office and 239,568 UA-assignee publications.
SELECT
  (SELECT COUNT(*) FROM `patents-public-data.patents.publications` WHERE country_code = 'UA') AS ua_office_pubs,
  (SELECT COUNT(*) FROM `patents-public-data.patents.publications` AS p
   WHERE EXISTS (SELECT 1 FROM UNNEST(p.assignee_harmonized) AS a WHERE a.country_code = 'UA')) AS ua_assignee_pubs;
