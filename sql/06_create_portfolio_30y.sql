-- Builds the project's own working table: filings since 1 Nov 1996, across all patent offices.
-- Later queries run on this small table instead of the 2.88 TB source.
-- Tables in the BigQuery sandbox expire after 60 days, so rerun this script to rebuild it.
CREATE SCHEMA IF NOT EXISTS nokia_analytics OPTIONS (location = 'US');

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
    WHERE REGEXP_CONTAINS(UPPER(a.name), r'NOKIA|ALCATEL|\bLUCENT\b|INFINERA|诺基亚|阿尔卡特|朗讯')
      AND NOT REGEXP_CONTAINS(UPPER(a.name), r'NOKIAN|ENOKIAN|AUTOLIV|MAILLEFER|SCANINTER|LUCENT (MEDICAL|SKY|TRANS|ADVANCED|BIOSCIENCES)|LUCENT OPTICS')
  ) AS owners,
  ARRAY(SELECT c.code FROM UNNEST(p.cpc) AS c) AS cpc_codes,
  (SELECT t.text FROM UNNEST(p.title_localized) AS t WHERE t.language = 'en' LIMIT 1) AS title_en
FROM `patents-public-data.patents.publications` AS p
WHERE p.filing_date >= 19961101
  AND EXISTS (
    SELECT 1
    FROM UNNEST(p.assignee_harmonized) AS a
    WHERE REGEXP_CONTAINS(UPPER(a.name), r'NOKIA|ALCATEL|\bLUCENT\b|INFINERA|诺基亚|阿尔卡特|朗讯')
      AND NOT REGEXP_CONTAINS(UPPER(a.name), r'NOKIAN|ENOKIAN|AUTOLIV|MAILLEFER|SCANINTER|LUCENT (MEDICAL|SKY|TRANS|ADVANCED|BIOSCIENCES)|LUCENT OPTICS')
  );
