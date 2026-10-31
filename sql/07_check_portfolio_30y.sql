-- Quick check of the working table: size, date range and coverage.
SELECT
  COUNT(*) AS publications,
  COUNT(DISTINCT application_number) AS applications,
  COUNT(DISTINCT family_id) AS families,
  COUNT(DISTINCT country_code) AS offices,
  MIN(filing_date) AS first_filing,
  MAX(filing_date) AS last_filing,
  COUNTIF(title_en IS NULL) AS without_english_title,
  COUNTIF(abstract_en IS NULL) AS without_english_abstract,
  COUNTIF(ARRAY_LENGTH(cpc_codes) = 0) AS without_cpc,
  COUNTIF(ARRAY_LENGTH(inventors) = 0) AS without_inventors,
  COUNTIF(ARRAY_LENGTH(inventor_countries) = 0) AS without_inventor_country,
  COUNTIF(ARRAY_LENGTH(cited_publications) = 0) AS without_citations
FROM nokia_analytics.portfolio_30y;
