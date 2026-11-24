# Progress and evidence tracker

The single record of what's done and what's left, checked against the [central research question](../01-research-design/research-design.md#central-research-question). Re-indexed 24 November 2026 after the factual audit.

## Status by research question

| Research question | Status | What stands between now and done |
|---|---|---|
| **RQ1.** Identify and classify relevant satcom patent families | In progress | Candidate pools exist and failed the 13 November diagnostic (70.8% vs the 85% project bar, agreement with software first-pass labels). Next: taxonomy redesign (capability vs attributes), fresh sample, human labelling |
| **RQ2.** Census families per company under the validated definitions | Blocked on RQ1 | Pre-validation census exists ([pool_census.csv](../../data/raw/pool_census.csv)); its SEC rows predate the 24 November SQL correction |
| **RQ3.** What the comparisons can tell us | Not started | Runs only on validated data |
| **Procurement.** Ukrainian government purchases of satellite-related equipment/services | In progress | Starlink extraction done (1,867 tenders, 4,050 plans); multi-category run in progress; contract details and document review not started |

## Done

| Item | Where |
|---|---|
| Patent extraction, name cleaning, family grouping (Nokia lineage + 5 satcom actors) | [`sql/`](../../sql/README.md), [`src/`](../../src) |
| Actor name census and review (11 names still undecided) | [satcom_name_review.csv](../../data/interim/satcom_name_review.csv) |
| Ukraine domestic-base search (scoped: candidate pools, this dataset) | [Queries 25–29](../../sql/README.md) |
| Candidate pool census (pre-validation) | [Query 32](../../sql/32_pool_census.sql) |
| Blind re-test with scoring pipeline | [Validation plan](../02-methodology/satcom-validation-plan.md#stage-3-result-13-november-2026-the-re-test-failed-the-bar) |
| Prozorro extractor + pipeline with checkpoints | [`src/prozorro_extractor.py`](../../src/prozorro_extractor.py), [`src/prozorro_pipeline.py`](../../src/prozorro_pipeline.py) |

## Remaining work, in order

| # | Step | Why first |
|---|---|---|
| 1 | Redesign the taxonomy: primary capability vs technology attributes (ISL, optical, anti-jamming, encryption) | Every comparison waits on it |
| 2 | Fresh stratified sample, human labelling, measure precision/recall against the 85% bar | Turns the diagnostic into validated accuracy |
| 3 | Rerun the census under the corrected rules; rerun the Ukraine search | Numbers must come from the validated pools |
| 4 | Decide the 11 flagged actor names | Finalises the comparison set |
| 5 | Ownership spot-check against registers | Counts are not verified rights |
| 6 | Procurement: finish the multi-category run, read a sample of tenders for requirements and final prices | Demand-side evidence for RQ-context |

## What can't be answered from public data

| Gap | How the docs handle it |
|---|---|
| Whether a company can reuse an invention, its engineering readiness, existing licences, internal deals | Not investigated; stated as out of scope |
| Starlink's real technological position | Stated as unmeasurable from patent counts |
| Classified defence R&D and procurement | Stated as invisible |
| Current ownership outside the US | Stated as a limit unless a free source turns up |

## Dropped deliberately

| Item | Why |
|---|---|
| Build–buy–partner–license matrix, ranked R&D priorities | Public data cannot support them; removed 24 November 2026 |
| Chi-square and trend tests on unvalidated pools | The validation gate forbids it |
| Ten-year maintenance cost model | [Parked](../../archive/parked-financial-analysis/) — feeds no current question |
