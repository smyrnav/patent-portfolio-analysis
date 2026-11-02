"""Write data/source_manifest.csv: which query or source produced each local snapshot, with its fingerprint."""
import hashlib

from common import ROOT, write_rows

GOOGLE = "patents-public-data.patents.publications, table last modified 23 Sep 2026"
SNAPSHOTS = [
    ("sql/01_owner_names.sql", "data/raw/owner_counts.csv", GOOGLE),
    ("sql/02_lineage_names.sql", "data/raw/lineage_counts.csv", GOOGLE),
    ("sql/03_filings_by_country.sql", "data/raw/filings_by_country.csv", GOOGLE),
    ("sql/04_check_us_kind_codes.sql", "data/raw/us_kind_codes.csv", GOOGLE),
    ("sql/05_owner_names_all_years.sql", "data/raw/owner_counts_all_years_top20.csv", GOOGLE),
    ("sql/07_check_portfolio_30y.sql", "data/raw/portfolio_30y_check.csv", "nokia_analytics.portfolio_30y"),
    ("sql/08_recount_us_30y.sql", "data/processed/us_30y_recount.csv", "nokia_analytics.portfolio_30y"),
    ("sql/09_family_status.sql", "data/processed/family_status.csv", "nokia_analytics.portfolio_30y"),
    ("sql/10_in_term_by_office.sql", "data/processed/in_term_by_office.csv", "nokia_analytics.family_status"),
    ("sql/11_new_families_by_year.sql and sql/12_office_filings_by_family.sql", "data/processed/office_filings_by_year.csv", "nokia_analytics.portfolio_30y"),
    ("sql/13_spot_check_sample.sql", "data/validation/spot_check_sample.csv", "nokia_analytics.portfolio_30y"),
    ("sql/14_mean_median_patent_measures.sql", "data/processed/patent_measures.csv", "nokia_analytics.portfolio_30y"),
    ("sql/16_codebook_sample.sql", "data/validation/codebook_sample.csv", "portfolio_30y and rivals_30y"),
    ("sql/17_codebook_sample_h04l49.sql", "data/validation/codebook_sample_h04l49.csv", "portfolio_30y and rivals_30y"),
    ("sql/18_validation_sample_metadata.sql and Google Patents pages, 1 Nov 2026", "data/validation/sample_metadata.csv", "portfolio_30y, rivals_30y and patents.google.com"),
    ("Hand-entered from Nokia 20-F reports, listed in data/raw/annual_reports_manifest.csv", "data/processed/nokia_financials_by_year.csv", "SEC EDGAR"),
    ("Hand-entered from company reports, sources in each row", "data/processed/commercial_context.csv", "SEC EDGAR and company sites"),
    ("AI first-pass labelling of Google Patents claims, 1 Nov 2026", "data/validation/manual_labels.csv", "patents.google.com"),
]


def fingerprint(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


if __name__ == "__main__":
    write_rows("data/source_manifest.csv", "produced_by snapshot source sha256".split(),
               [(query, path, source, fingerprint(path)) for query, path, source in SNAPSHOTS])
    print(f"Manifest covers {len(SNAPSHOTS)} snapshots.")
