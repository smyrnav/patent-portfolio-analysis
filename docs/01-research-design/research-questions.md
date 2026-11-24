# Research questions

Three questions support the [central research question](research-design.md#central-research-question). Adopted 24 November 2026 after the factual audit; the previous reuse-and-dependencies framing is retired because it promised conclusions public data cannot establish.

| # | Research question | How it's answered | Output | Status |
|---|---|---|---|---|
| **RQ1** | How can relevant satellite-communications patent families be identified and classified? | Candidate CPC pools, then claims review of samples against the 85% acceptance bar | A classification method whose error rate is measured, per pool | In progress. The 13 November re-test failed at 70.8% agreement with software first-pass labels; taxonomy redesign is next |
| **RQ2** | What patent families are associated with Nokia, ICEYE and selected competitors under the resulting definitions? | Family census per company and pool on the cleaned tables | Portfolio counts with their confidence labels | Blocked on RQ1. Pre-validation census exists ([pool_census.csv](../../data/raw/pool_census.csv)) |
| **RQ3** | What can the resulting comparisons tell us, and what would require further investigation? | Pool comparisons on validated data, plus the gap list | Findings, each labelled observation, hypothesis or conclusion | Not started |

Procurement is a separate question with its own data and methods:

> **What do Ukrainian public procurement records show about government purchases and planned purchases of satellite-related equipment and services?**

Documented in [procurement-demand.md](procurement-demand.md). It answers a demand-side question; it is not evidence about patent ownership or technical capability.

## The validation gate

No comparative claim between companies may use a pool that hasn't passed the [85% precision bar](../02-methodology/satcom-validation-plan.md) on human-reviewed labels. The bar is a project acceptance rule, not an industry standard. The 13 November re-test measured 70.8% agreement between the CPC-based sorting and software-generated first-pass labels on a blind 144-patent sample — a diagnostic result that says the current rules are not reliable enough, not a validated accuracy figure. Human review is the missing stage; the taxonomy redesign comes first, then a fresh sample, then human labelling.

## Retired questions

Kept for the record; they do not guide current work.

| Retired | Why |
|---|---|
| Which capabilities and investment priorities matter most | Public data cannot rank a company's internal investment decisions |
| What can the partners reuse, develop or acquire | Reuse depends on engineering capability, existing licences and the partnership's undisclosed internal agreements — none visible in patent records |
| Build–buy–partner–license per capability, ranked R&D priorities | Same reason. Removed, not parked |

## Hypotheses

The satcom hypotheses live in [satcom-hypotheses.md](satcom-hypotheses.md), gated by the validation plan: they may run only on precision-adjusted or hand-labelled data. The pre-pivot H1–H4 (optical/routing/switching) are retired with their scope and preserved in git history.

## What public data can't settle

Patents show disclosed inventions, not product quality, engineering readiness or market share. The partnership's division of work, existing licences and development costs are invisible from outside. Where the data ends, the docs say so.
