# Findings so far

**There's no answer to the central question yet.** These are provisional findings, in the [required format](../01-research-design/research-design.md#how-to-state-an-answer). The executive brief gets written once RQ2 and RQ3 have validated evidence behind them.

Mapped to the [three research questions](../01-research-design/research-questions.md) adopted 24 November 2026. Pre-pivot findings 1–5 (optical/routing/switching) are [archived](../../archive/pre-pivot/findings-pre-pivot.md) as the method demonstration.

## Satcom findings (post-pivot)

### S1. Ukraine has no domestic satellite-communications patent base — feeds RQ1 and RQ3
- **Evidence:** 16 Ukrainian-assignee names in the satcom pools, all individual inventors with one family each ([query 25](../../sql/25_ukraine_satcom_assignees.sql)); 10 owners ever filed satcom patents at the Ukrainian office, 16 families total ([query 26](../../sql/26_ukraine_office_satcom_filings.sql)). Coverage check: 336,474 Ukrainian-office publications exist in the dataset ([query 27](../../sql/27_ukraine_coverage_check.sql)), so the empty result is real, not a data hole.
- **Confidence:** high for the pools as defined; they are candidates, so this gets rerun after validation.
- **What would change it:** validation broadening the pools, or classified defence R&D that never patents (invisible by design).
- **Decision:** domestic sourcing of the patented technology is eliminated as an option; the system will run on foreign-patented technology, which makes licensing and partnership terms central to the sovereignty question. Note the boundary: this is a statement about the patent base, not about Ukrainian engineering capability, which patents do not measure.

### S2. ICEYE's patent record is radar- and platform-heavy, comms-thin — feeds RQ1 and RQ2
- **Evidence:** 53 ICEYE simple families in the peers table (all 9 name variants checked; ~70 families across variants before family-level deduplication), dominated by radar (G01S, 35) and spacecraft-platform (B64G, 14) codes, with 7 in transmission (H04B); the read example [WO2025252651A1](https://patents.google.com/patent/WO2025252651A1/en) is a radar antenna, not communications ([queries 24, 35, 36](../../sql/README.md)).
- **Confidence:** medium-high for the direction; the per-pool census is pending.
- **What would change it:** the pool census showing validated comms families, or ICEYE keeping comms work as trade secrets.
- **Hypothesis, not a finding:** the partnership's communications IP would come from Nokia. The actual division of engineering work and IP ownership between the partners is undisclosed, and a thin public patent record does not prove a thin capability. This stays a hypothesis until RQ1's capability map or a disclosure tests it.

### S3. The incumbents' patent positions are deep — feeds RQ3
- **Evidence:** peers table counts — Airbus 19,488 families, Thales 9,873, Viasat 822, Eutelsat/OneWeb 110, ICEYE 53 ([query 24](../../sql/24_satcom_peers_30y.sql)).
- **Confidence:** high on ownership of the counts (exact-name review, 11 names still pending a keep/drop decision); what is inside those families awaits the pool census.
- **What would change it:** the census showing the depth sits outside the five capabilities.
- **Decision:** the dependency analysis (RQ3) is a core deliverable, not a formality.

### S4. Patent data cannot see the market leader — a limit on all of RQ2 and RQ3
- **Evidence:** SpaceX holds 110 patent families against Airbus's 19,488 ([query 30](../../sql/30_spacex_name_counts.sql)) — a trade-secret strategy, not a technology gap.
- **Confidence:** high as a patent-count fact.
- **What would change it:** nothing on the patent side; ETSI declarations and procurement data would complement later.
- **Decision:** no Starlink benchmark from patent counts, and say so wherever comparisons are made.
