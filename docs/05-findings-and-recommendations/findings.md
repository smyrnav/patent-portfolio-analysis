# Findings so far

**There's no answer to the central question yet.** These are provisional findings, in the [required format](../01-research-design/research-design.md#how-to-state-an-answer). The executive brief gets written once RQ5 has evidence behind it.

## Satcom findings (post-pivot)

### S1. Ukraine has no domestic satellite-communications patent base
- **Evidence:** 16 Ukrainian-assignee names in the satcom pools, all individual inventors with one family each ([query 25](../../sql/25_ukraine_satcom_assignees.sql)); 10 owners ever filed satcom patents at the Ukrainian office, 16 families total ([query 26](../../sql/26_ukraine_office_satcom_filings.sql)). Coverage check: 336,474 Ukrainian-office publications exist in the dataset ([query 27](../../sql/27_ukraine_coverage_check.sql)), so the empty result is real, not a data hole.
- **Confidence:** high for the pools as defined; they are candidates, so this gets rerun after validation.
- **What would change it:** validation broadening the pools, or classified defence R&D that never patents (invisible by design).
- **Decision:** RQ4 treats "buy or license domestically" as eliminated; the system's technology will be foreign-patented, which makes licensing terms central.

### S2. ICEYE's patent record is radar- and platform-heavy, comms-thin
- **Evidence:** 53 ICEYE families in the peers table, dominated by radar (G01S) and spacecraft-platform (B64G) codes; the read example [WO2025252651A1](https://patents.google.com/patent/WO2025252651A1/en) is a radar antenna, not communications.
- **Confidence:** medium-high for the direction; the per-pool census is pending.
- **What would change it:** the pool census showing validated comms families, or ICEYE keeping comms work as trade secrets.
- **Decision:** the partnership's communications IP would come from Nokia; ICEYE's contribution is satellites and radar.

### S3. The incumbents' patent positions are deep
- **Evidence:** peers table counts — Airbus 19,488 families, Thales 9,873, Viasat 822, Eutelsat/OneWeb 110, ICEYE 53 ([query 24](../../sql/24_satcom_peers_30y.sql)).
- **Confidence:** high on ownership of the counts (exact-name review); what is inside those families awaits the pool census.
- **What would change it:** the census showing the depth sits outside the five capabilities.
- **Decision:** the exposure analysis (RQ2) is a core deliverable, not a formality.

### S4. Patent data cannot see the market leader
- **Evidence:** SpaceX holds 110 patent families against Airbus's 19,488 ([query 30](../../sql/30_spacex_name_counts.sql)) — a trade-secret strategy, not a technology gap.
- **Confidence:** high as a patent-count fact.
- **What would change it:** nothing on the patent side; ETSI declarations and procurement data would complement later.
- **Decision:** no Starlink benchmark from patent counts, and say so wherever comparisons are made.

## Pre-pivot findings (method demonstration)

Findings 1–5 below predate the 2 November 2026 pivot and answer the old optical/routing/switching question. They stand as evidence of method, not as answers to the satcom question.

## 1. Patent codes can't be used alone to compare companies

- **Evidence:** claims earned the matching class in [73 of 100 optical, 39 of 100 routing and 42 of 100 H04L 49 patents](../02-methodology/validation.md#precision-result), against my 85% bar. Precision also [falls in newer patents](../02-methodology/validation.md#precision-by-priority-period).
- **Confidence:** medium. The gaps are large, but the labels are a software-generated first pass; human review and human–software agreement aren't done.
- **What would change it:** independent human hand-labels disagreeing with the first pass, or a looser rule on control-plane claims.
- **Decision:** use claim-based estimates with ranges, and stop using raw code counts.

## 2. A large share of Nokia-lineage patents may be held by others, unlike the other four companies

- **Evidence:** [42 of 179 sampled patents (23.5%)](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) show another current assignee on Google Patents, against 2 of 242 for the others.
- **Confidence:** medium for the direction, low for the size. Google Patents isn't a register, and the sample covers three technologies.
- **What would change it:** USPTO assignment records on a random US sample showing a much lower share.
- **Decision:** investigate before any cost or comparison work uses applicant counts. Report Nokia with and without these patents.

## 3. Nokia's lineage looks strongest in optical and thinnest in switching

- **Evidence:** [estimated US families](../03-market-and-patent-analysis/patent-landscape.md#estimated-us-families-by-company) of 768 optical, 233 routing and 70 switching. Cisco has an estimated 792 in routing and 220 in switching.
- **Confidence:** low. Samples are small, recall isn't tested, and the figures cover all years rather than 2020–2024.
- **What would change it:** recall results, current-owner checks or claim-based 2020–2024 shares.
- **Decision:** investigate routing and switching first as possible exposures.

## 4. The candidate universe isn't a verified portfolio

- **Evidence:** [19,873 families with grant evidence and 5,595 families with a recent application and no grant detected](../02-methodology/candidate-portfolio-universe.md), with no verified active rights or current owners yet. The [saved US recount](../03-market-and-patent-analysis/patent-landscape.md#where-nokias-patents-came-from) verifies 36,630 distinct publications and 37,710 owner-publication listings. Origin counts overlap, so a distinct Alcatel/Lucent share awaits a corrected publication-level SQL rerun.
- **Confidence:** high that it isn't verified. The size of the gap is unknown.
- **What would change it:** register checks.
- **Decision:** base the [cost model](../04-financial-analysis/ten-year-maintenance-cost-model.md) on verified sampled rights, not on these counts.

## 5. Market leadership differs by segment

- **Evidence:** [segment figures](../03-market-and-patent-analysis/market-context-and-peer-selection.md#segment-figures-behind-the-map): Huawei and Ciena lead in optical transport, Cisco in routers and all Ethernet switching, NVIDIA in data centre Ethernet, and Celestica in Ethernet AI back-end.
- **Confidence:** high for the published figures, with some from trade coverage of paid reports.
- **What would change it:** new market reports, as periods differ.
- **Decision:** compare by technology, not by company total.
