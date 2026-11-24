# Progress and evidence tracker

The single record of what's done and what's left, checked against the [central research question](../01-research-design/research-design.md#central-research-question). Status: ✅ done · 🟡 partly done · ❌ not started or missing.

Re-indexed 24 November 2026 to the [three research questions](../01-research-design/research-questions.md); the old RQ4/RQ5 rows are retired, and the financial workstream is [parked](../../archive/parked-financial-analysis/).

## Evidence by research question

| Research question | Needs most | Status |
|---|---|---|
| **RQ1.** System capabilities and each partner's demonstrable contribution | Desk research on partnership disclosures mapped to system components; [Ukraine satcom context](deep-research-ukraine-satcom.md) gathered; [procurement demand evidence](../01-research-design/procurement-demand.md) proposed as the real-requirements check | 🟡 |
| **RQ2.** Validated patent landscape | Peers table built ✅; Ukraine domestic base answered ✅; **blocked on classification validation** (re-test failed at 70.8% on 13 November); [owner evidence](questions.md#q22-how-much-of-the-portfolio-i-attribute-to-nokia-does-it-still-own) open | 🟡 |
| **RQ3.** Third-party concentrations and due-diligence priorities | RQ2's validated counts, then [H1–H3](../01-research-design/satcom-hypotheses.md) on precision-adjusted data | ❌ |

## Evidence in detail

| Part of the question | Evidence needed | Nokia | Competitors | What's missing |
|---|---|---|---|---|
| **Who to compare** | Satcom actor set with reviewed name mapping | ✅ [Name review](../../data/interim/satcom_name_review.csv) and [peers table](../../sql/24_satcom_peers_30y.sql) | ✅ Same | 11 flagged names, my decision. Pre-pivot [peer selection](../../archive/pre-pivot/market-context-and-peer-selection.md) kept as method record |
| **Ukraine domestic patent base** | Ukrainian satcom holders and Ukraine-office filings | ✅ [Answered: no corporate base](../../sql/25_ukraine_satcom_assignees.sql) | ✅ [10 foreign owners ever](../../sql/26_ukraine_office_satcom_filings.sql) | Rerun after pool validation |
| **Technology position** | Families per satcom pool, tested against claims | 🟡 Pre-pivot [first estimates](../../archive/pre-pivot/patent-landscape.md) (method demonstration) | 🟡 Same; [peers table](../../sql/24_satcom_peers_30y.sql) built | Pool census, then precision and recall checks |
| **Growth** | New families by class and year | ❌ | ❌ | Claim-based estimates by period |
| **Patent age** | Families reaching 20 years by 2036 | 🟡 Dates exist, not by class | ❌ | Same as above |
| **Market coverage** | Filings in the US, Europe, China and Japan | 🟡 [Totals exist](../../archive/pre-pivot/twenty-years.md), not by class | ❌ | Same as above |
| **Verified rights and owners** | Renewals and transfers | 🟡 [Sample warning only](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) | 🟡 Same sample | USPTO renewal and assignment records |
| **Commercial context: R&D** | R&D by year, with boundaries stated | ✅ [20 years](../../archive/pre-pivot/twenty-years.md) | 🟡 [Latest period](../../archive/pre-pivot/market-context-and-peer-selection.md#commercial-context) | Earlier years, and Huawei's report. Not for ranking |
| **Findings and recommendations** | Findings tied to decisions | 🟡 [Provisional](../05-findings-and-recommendations/findings.md) | N/A | Depends on everything above |

## What to do, in order

| # | Step | Why | Research action / human review | Cost | Status |
|---|---|---|---|---|---|
| 0 | Re-aim the central question to reuse, dependencies and due diligence; archive pre-pivot and park financial work | The old five-question structure outran the evidence | Researcher decision | None | ✅ 24 November 2026 |
| 1 | Preserve the research question, and add the public-data qualification | Everything else depends on it | Researcher decision | None | ✅ |
| 2 | Unify the [technology scope](../01-research-design/scope.md) | Documents disagreed on switching | Researcher decision | None | ✅ |
| 3 | Correct [portfolio terminology](../02-methodology/candidate-portfolio-universe.md#what-each-data-category-establishes) | Counts were being read as ownership | Researcher decision | None | ✅ |
| 4 | Complete classification validation: preliminary software pilot and precision are done. **Next is the taxonomy redesign** (separate primary capability from technology attributes such as inter-satellite links), a new stratified sample, human hand-labelling, human–software agreement, repeated-subset consistency and recall. [60-publication sheet](../../data/validation/agreement_sheet.csv) | Needed for every comparison | Human hand-labelling, evidence review and adjudication required; software-assisted sampling only | Free, from Google Patents pages | 🟡 |
| 5 | Estimate how much of the universe has been transferred, on a random US sample and USPTO assignment records | [23.5% in my sample](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) | Researcher obtains USPTO records and reviews assignment evidence | Free | ❌ |
| 6 | Run the register spot-check on [35 patents](../../data/validation/spot_check_sample.csv) | Shows the error rate | Researcher checks official registers and reviews all outputs | Free | ❌ |
| 7 | Build the RQ1 capability map from partnership disclosures | The reuse answer needs a shared picture of the system | Researcher desk research with cited sources | None | ❌ |
| 7a | Extract the [procurement evidence](../01-research-design/procurement-demand.md): 1,867 Starlink tenders pulled via [`prozorro_extractor`](../../src/prozorro_extractor.py); next is reading a sample for requirements and final prices | Real buyer requirements, independent of the blocked patent work | Researcher reads tenders and validates the extraction sheet | None | 🟡 |
| 8 | Build comparable portfolios by pool and period, and test H1–H3 | Answers RQ2–RQ3 | Software-assisted processing; researcher validates methods and outputs | Small | ❌ gated by step 4 |
| 9 | Decide the 11 flagged satcom names | Finalises the comparison set | Researcher decision | None | ❌ |
| 10 | Write findings and the executive brief | Answers RQ2–RQ3 | Researcher writes and approves findings | None | 🟡 |
| — | ~~Re-aim commercial alignment to satcom~~ | Pre-pivot version [archived](../../archive/pre-pivot/commercial-alignment.md); a satcom version starts only if RQ1 shows a need | — | — | Parked |
| — | ~~Complete the Q9 ten-year cost model~~ | [Parked](../../archive/parked-financial-analysis/) with the retired investment-priorities question | — | — | Parked |

## Other open items

| Item | Status |
|---|---|
| Why reported families fell and rose ([Q20](questions.md#q20-why-did-nokias-reported-portfolio-fall-from-26000-to-about-20000-then-return-to-26000)) | Unexplained, and Q22 may help |
| Some tables cite report names rather than links | To fix |
| My [knowledge checklist](explain-it.md#do-it-myself) | Unfinished |
| Motivation letter needs a real work example from me | Outside this repo |

## What I can drop

| Item | Why |
|---|---|
| ETSI declarations | The comparison doesn't depend on them. They matter for licensing and AI-RAN, so they can wait |
| AI-RAN, 6G and licensing database | [Parked](../01-research-design/scope.md#parked) |
| More annual report extraction for Nokia | Enough for now, apart from checking the figures |
| Chi-square and ranked investment scoring on unvalidated pools | The [validation gate](../01-research-design/research-questions.md#the-validation-gate) forbids it; statistics on bad labels is worse than no statistics |

## What can't be answered from public data

| Gap | How the answer handles it |
|---|---|
| Nokia's and competitors' patent budgets | Statutory fee estimates, with assumptions labelled |
| The partnership's division of engineering work and IP ownership | Stated as undisclosed wherever it matters |
| Value of individual patents | Scenarios and indicators, never stated as fact |
| Technical quality of products and engineering readiness | Out of scope |
| Current ownership outside the US | Stated as a limit, unless a free source turns up |

## Minimum for a defensible answer

The essentials are step 4 (taxonomy redesign and validation test #3), then steps 7–10. Nothing comparative ships before step 4 passes; that is the gate, not a courtesy.
