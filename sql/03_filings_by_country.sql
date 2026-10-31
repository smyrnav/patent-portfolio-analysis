-- Where the Nokia family's patent applications were filed.
-- EP is the European Patent Office, not the EU. Chinese-language names are included for CN records.
-- grant_date may be incomplete outside the US, so check granted_applications before trusting it.
SELECT
  p.country_code,
  COUNT(DISTINCT p.application_number) AS applications,
  COUNT(DISTINCT IF(p.grant_date > 0, p.application_number, NULL)) AS granted_applications,
  COUNT(DISTINCT p.family_id) AS patent_families
FROM `patents-public-data.patents.publications` AS p,
  UNNEST(p.assignee_harmonized) AS a
WHERE REGEXP_CONTAINS(
    UPPER(a.name),
    r'\bNOKIA\b|\bALCATEL\b|\bLUCENT TECHNOLOGIES\b|\bINFINERA\b|诺基亚|阿尔卡特|朗讯'
  )
GROUP BY p.country_code
ORDER BY applications DESC;
