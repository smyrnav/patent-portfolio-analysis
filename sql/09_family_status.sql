-- Sorts all families by grant evidence, using the working table only. Grant evidence is not current legal status:
-- rights may have lapsed or transferred, and grant_date is incomplete outside the US.
-- Saved CSV snapshots predate this office-aware heuristic and the clarified status labels.
CREATE OR REPLACE TABLE nokia_analytics.family_status AS
WITH pubs AS (
    SELECT family_id, country_code, kind_code, filing_date,
        EXISTS(
            SELECT 1 FROM UNNEST(owners) AS o
            WHERE NOT REGEXP_CONTAINS(UPPER(o), r'TCL|OPTRONICS|KABEL|CABLE|FIBRES|MOBILE COMM|RADIOTELEPHONE|SUBMARCOM|SUBMARINE')
        ) AS core_owner,
        CASE
            WHEN country_code = 'WO' THEN FALSE
            WHEN country_code = 'US' THEN grant_date > 0 AND REGEXP_CONTAINS(kind_code, r'^[ABE]')
            WHEN country_code = 'EP' THEN STARTS_WITH(kind_code, 'B')
            WHEN country_code = 'CN' THEN REGEXP_CONTAINS(kind_code, r'^[BC]')
            WHEN country_code = 'JP' THEN grant_date > 0
            WHEN NOT STARTS_WITH(kind_code, 'S') THEN grant_date > 0
            ELSE FALSE
        END AS grant_evidence
    FROM nokia_analytics.portfolio_30y
)
-- Legacy field names are retained for downstream compatibility; they represent grant evidence, not legal status.
SELECT family_id,
    LOGICAL_OR(core_owner) AS core_owner,
    LOGICAL_OR(grant_evidence) AS ever_granted,
    LOGICAL_OR(grant_evidence AND filing_date >= 20061101) AS granted_in_term,
    LOGICAL_OR(NOT grant_evidence AND country_code != 'WO' AND filing_date >= 20210101) AS recent_application,
    LOGICAL_OR(country_code = 'US' AND grant_evidence AND filing_date >= 20061101) AS us_in_term,
    COUNT(DISTINCT IF(grant_evidence AND filing_date >= 20061101, country_code, NULL)) AS offices_in_term,
    MIN(filing_date) AS first_filing,
    MAX(filing_date) AS last_filing
FROM pubs
GROUP BY family_id;

SELECT CASE
    WHEN NOT core_owner THEN '5 Sold-business names only'
    WHEN granted_in_term THEN '1 Grant evidence, within 20 years'
    WHEN recent_application THEN '2 Recent application, no grant detected'
    WHEN ever_granted THEN '3 Grant evidence, past 20 years'
    ELSE '4 No grant detected, older filing'
END AS status,
    COUNT(*) AS families,
    COUNTIF(us_in_term) AS with_us_in_term,
    ROUND(AVG(offices_in_term), 2) AS avg_offices_in_term
FROM nokia_analytics.family_status
GROUP BY status
ORDER BY status;
