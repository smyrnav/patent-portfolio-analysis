# Saved queries

Numbered in the order I ran them, as the exact text used, so older queries keep older wording such as "owners" and "core". Sandbox tables expire after 60 days, so results are saved locally, and [`data/source_manifest.csv`](../data/source_manifest.csv) fingerprints them. A cell-by-cell archive is in [`notebooks/patent_portfolio_queries.ipynb`](../notebooks/patent_portfolio_queries.ipynb).

| Query | Purpose | Saved result | Data scanned |
|---|---|---|---|
| [01](01_owner_names.sql) | Applicant names with Nokia or Alcatel | [`owner_counts.csv`](../data/raw/owner_counts.csv) | Not recorded |
| [02](02_lineage_names.sql) | Lucent, Infinera and other lineage names | [`lineage_counts.csv`](../data/raw/lineage_counts.csv) | Not recorded |
| [03](03_filings_by_country.sql) | Applications by office | [`filings_by_country.csv`](../data/raw/filings_by_country.csv) | Not recorded |
| [04](04_check_us_kind_codes.sql) | US kind code check | [`us_kind_codes.csv`](../data/raw/us_kind_codes.csv) | Not recorded |
| [05](05_owner_names_all_years.sql) | Names across all years | [`owner_counts_all_years_top20.csv`](../data/raw/owner_counts_all_years_top20.csv), top 20 only | Not recorded |
| [06](06_create_portfolio_30y.sql) | Builds the Nokia-lineage table | Table `portfolio_30y` | About 289 GB |
| [07](07_check_portfolio_30y.sql) | Checks that table | [`portfolio_30y_check.csv`](../data/raw/portfolio_30y_check.csv) | Not recorded |
| [08](08_recount_us_30y.sql) | US recount | [`us_30y_recount.csv`](../data/processed/us_30y_recount.csv) | 14.46 MB |
| [09](09_family_status.sql) | Sorts families by status | [`family_status.csv`](../data/processed/family_status.csv) | About 15 MB |
| [10](10_in_term_by_office.sql) | Grant evidence by office | [`in_term_by_office.csv`](../data/processed/in_term_by_office.csv) | Not recorded |
| [11](11_new_families_by_year.sql), [12](12_office_filings_by_family.sql) | Families and filings by year | [`office_filings_by_year.csv`](../data/processed/office_filings_by_year.csv) | Not recorded |
| [13](13_spot_check_sample.sql) | Register spot-check sample | [`spot_check_sample.csv`](../data/validation/spot_check_sample.csv) | Not recorded |
| [14](14_mean_median_patent_measures.sql) | Time to grant and filings per family | [`patent_measures.csv`](../data/processed/patent_measures.csv) | Not recorded |
| [15](15_rivals_30y.sql) | Builds the competitor table | Table `rivals_30y` | 43.9 GB |
| [16](16_codebook_sample.sql) | Validation sample | [`codebook_sample.csv`](../data/validation/codebook_sample.csv) | Not recorded |
| [17](17_codebook_sample_h04l49.sql) | H04L 49-only sample | [`codebook_sample_h04l49.csv`](../data/validation/codebook_sample_h04l49.csv) | Not recorded |
| [18](18_validation_sample_metadata.sql) | Family and priority date for the labelled sample | [`sample_metadata.csv`](../data/validation/sample_metadata.csv) | Not recorded |
