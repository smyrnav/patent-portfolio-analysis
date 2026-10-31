-- New families per year, using the first filing date in the working table. This is part of the exact query I ran.
SELECT DIV(first_filing, 10000) AS yr, COUNT(*) AS new_families FROM nokia_analytics.family_status GROUP BY yr ORDER BY yr;
