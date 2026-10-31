-- Working table: filings since 1 Nov 1996, across all patent offices.
-- Later queries use this small table instead of the 2.88 TB source.
-- Sandbox tables expire after 60 days, so rerun this to rebuild it.
CREATE SCHEMA IF NOT EXISTS nokia_analytics
  OPTIONS (location = 'US');

CREATE TEMP FUNCTION is_family(n STRING) AS (
  (
    REGEXP_CONTAINS(UPPER(n), r'NOKIA|ALCATEL|\bLUCENT\b|INFINERA')
    OR REGEXP_CONTAINS(n, r'诺基亚|阿尔卡特|朗讯|ノキア|노키아')
  )
  AND NOT REGEXP_CONTAINS(UPPER(n), r'NOKIAN|ENOKIAN|AUTOLIV')
  AND NOT REGEXP_CONTAINS(UPPER(n), r'MAILLEFER|SCANINTER')
  AND NOT REGEXP_CONTAINS(UPPER(n), r'LUCENT (MEDICAL|SKY|TRANS)')
  AND NOT REGEXP_CONTAINS(UPPER(n), r'LUCENT (ADVANCED|BIOSCIENCES)')
  AND NOT REGEXP_CONTAINS(UPPER(n), r'LUCENT OPTICS')
);

CREATE OR REPLACE TABLE nokia_analytics.portfolio_30y AS
SELECT
  p.publication_number,
  p.application_number,
  p.family_id,
  p.country_code,
  p.kind_code,
  p.priority_date,
  p.filing_date,
  p.publication_date,
  p.grant_date,
  ARRAY(
    SELECT DISTINCT a.name
    FROM UNNEST(p.assignee_harmonized) AS a
    WHERE is_family(a.name)
  ) AS owners,
  ARRAY(
    SELECT DISTINCT i.country_code
    FROM UNNEST(p.inventor_harmonized) AS i
    WHERE i.country_code != ''
  ) AS inventor_countries,
  ARRAY(SELECT c.code FROM UNNEST(p.cpc) AS c) AS cpc_codes,
  (
    SELECT t.text
    FROM UNNEST(p.title_localized) AS t
    WHERE t.language = 'en'
    LIMIT 1
  ) AS title_en
FROM `patents-public-data.patents.publications` AS p
WHERE p.filing_date >= 19961101
  AND EXISTS (
    SELECT 1
    FROM UNNEST(p.assignee_harmonized) AS a
    WHERE is_family(a.name)
  );
