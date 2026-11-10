-- Recent ICEYE publications from the peers table, for the claims-reading
-- rehearsal in the validation docs (WO2025252651A1, the SAR antenna patent).
-- Runs on the sandbox table nokia_analytics.satcom_peers_30y (query 24).
SELECT
  publication_number,
  filing_date,
  title_en,
  (SELECT STRING_AGG(code) FROM UNNEST(cpc_codes) AS code) AS cpc
FROM nokia_analytics.satcom_peers_30y
WHERE 'ICEYE' IN UNNEST(owners)
ORDER BY filing_date DESC
LIMIT 8;
