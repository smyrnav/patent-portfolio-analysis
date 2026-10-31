-- Quick check of the working table: size, date range and coverage.
SELECT
  COUNT(*) AS publications,
  COUNT(DISTINCT application_number) AS applications,
  COUNT(DISTINCT family_id) AS families,
  COUNT(DISTINCT country_code) AS offices,
  MIN(filing_date) AS first_filing,
  MAX(filing_date) AS last_filing,
  COUNTIF(title_en IS NULL) AS without_english_title,
  COUNTIF(ARRAY_LENGTH(cpc_codes) = 0) AS without_cpc
FROM nokia_analytics.portfolio_30y;
