# Findings so far

**The central question is not answered yet.** What follows separates observations (what the data shows), hypotheses (possible explanations) and what remains unverified. Pre-pivot findings are [archived](../../archive/pre-pivot/findings-pre-pivot.md).

## Observations

### O1. Within this search scope, no Ukrainian corporate assignees appear in the candidate satcom pools
- **Evidence:** 16 Ukrainian-assignee names in the candidate pools, all individual inventors with one family each ([query 25](../../sql/25_ukraine_satcom_assignees.sql)); 10 owners ever filed satcom-pool patents at the Ukrainian office, 16 families total ([query 26](../../sql/26_ukraine_office_satcom_filings.sql)); 336,474 Ukrainian-office publications exist in the dataset, so the empty result is not a data hole ([query 27](../../sql/27_ukraine_coverage_check.sql)).
- **Scope of the claim:** these candidate pools and name-matching rules, in this dataset, as of the query dates. It says nothing about Ukrainian engineering capability, classified work, or companies that never patent. The pools themselves are unvalidated, so this gets rerun after validation.

### O2. Company-level patent-family totals in the dataset
- **Evidence:** [query 24](../../sql/24_satcom_peers_30y.sql) — Airbus 19,488, Thales 9,873, Viasat 822, Eutelsat/OneWeb 110, ICEYE 53 simple families, exact-name matched, filings since 1996.
- **Scope of the claim:** these are **all-technology** counts (name and filing date only, no CPC filter). They describe overall portfolio size in the dataset, not satellite-communications positions. Using them as satcom comparisons would be an error.

### O3. CPC-candidate satcom counts (unvalidated)
- **Evidence:** [query 32](../../sql/32_pool_census.sql) / [pool_census.csv](../../data/raw/pool_census.csv) — candidate families across the five pools: Nokia lineage 576, Thales 343, Viasat 307, Airbus 188, Eutelsat/OneWeb 53, ICEYE 6.
- **Scope of the claim:** these counts are what the candidate CPC codes catch. The 13 November re-test showed the codes catch the wrong patents about 3 times in 10, so these numbers are not reliable portfolio comparisons. The saved SEC rows were computed under a rule inconsistent with decision R1 and regenerate differently (corrected 24 November 2026).

### O4. A name search finds 110 SpaceX-associated patent families
- **Evidence:** [query 30](../../sql/30_spacex_name_counts.sql) — 366 publications, 110 families.
- **Scope of the claim:** an applicant-name match count. These are not "110 Starlink patents", and the number alone does not prove a deliberate trade-secret strategy. What it establishes: Starlink's technological position cannot be measured through these patent counts, so no patent-based comparison with Starlink is made anywhere in this project.

### O5. The classification does not meet its acceptance bar
- **Evidence:** the 13 November re-test on a blind 144-patent sample: 102/144 = 70.8% agreement between CPC-based sorting and software-generated first-pass labels, against the project's 85% acceptance rule ([full record](../02-methodology/satcom-validation-plan.md#stage-3-result-13-november-2026-the-re-test-failed-the-bar)).
- **Scope of the claim:** this is a diagnostic against software first-pass labels, not independently measured accuracy — human review is not done. Consequence: every company comparison stays blocked until the taxonomy is redesigned and a fresh sample passes with human-reviewed labels.

## Hypotheses (untested)

- **ICEYE's portfolio is radar- and platform-heavy, comms-thin.** Preliminary applicant-name and CPC-class results: of 53 families, CPC classes G01S (radar) on 35, B64G (spacecraft operations) on 14, H04B (transmission) on 7 ([queries 35, 36](../../sql/README.md)); 6 families fall in the candidate satcom pools. These are classification-level results, not verified capabilities, and overlapping CPC classes mean a family can count in several classes. The further guess that the partnership's comms IP comes from Nokia remains a guess: the actual split is undisclosed.
- **SpaceX protects technology as trade secrets.** Consistent with the small patent count and with public reporting, but not established by it.

## What remains unverified

- Current ownership of any counted patent (register/assignment checks not done).
- Whether any candidate pool, once redesigned, passes the 85% bar with human-reviewed labels.
- The 11 flagged satcom actor names awaiting a keep/drop decision.
