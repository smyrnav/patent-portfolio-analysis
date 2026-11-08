# Progress and evidence tracker

The single record of what's done and what's left, checked against the [central research question](../01-research-design/research-design.md#central-research-question). Status: ✅ done · 🟡 partly done · ❌ not started or missing.

## Evidence by research question

| Research question | Needs most | Status |
|---|---|---|
| **RQ1.** Reusable Nokia–ICEYE assets | Validated pools; census on the Nokia-lineage and ICEYE tables; [owner evidence](questions.md#q22-how-much-of-the-portfolio-i-attribute-to-nokia-does-it-still-own) | ❌ |
| **RQ2.** Third-party exposure | New peers table (name research first), then [H1](../01-research-design/satcom-hypotheses.md) on precision-adjusted counts | ❌ |
| **RQ3.** Where competitors invest and where differentiation is possible | Period-stratified counts (H2), citation context (H3) | ❌ |
| **RQ4.** Build, buy, partner or license per capability | RQ1–RQ3 plus desk research on licensing and acquisition precedents | ❌ |
| **RQ5.** R&D funding priorities | All of the above, plus the Q9 cost range | ❌ |

## Evidence in detail

| Part of the question | Evidence needed | Nokia | Competitors | What's missing |
|---|---|---|---|---|
| **Who to compare** | Market leaders by segment | ✅ [Checked](../03-market-and-patent-analysis/market-context-and-peer-selection.md) | ✅ [Checked](../03-market-and-patent-analysis/market-context-and-peer-selection.md) | Nothing essential |
| **Technology position** | Families by class, tested against claims | 🟡 [First estimates](../03-market-and-patent-analysis/patent-landscape.md) | 🟡 [First estimates](../03-market-and-patent-analysis/patent-landscape.md) | Agreement test and recall |
| **Growth** | New families by class and year | ❌ | ❌ | Claim-based estimates by period |
| **Patent age** | Families reaching 20 years by 2036 | 🟡 Dates exist, not by class | ❌ | Same as above |
| **Market coverage** | Filings in the US, Europe, China and Japan | 🟡 [Totals exist](../03-market-and-patent-analysis/twenty-years.md), not by class | ❌ | Same as above |
| **What Infinera added** | Nokia with and without Infinera | 🟡 Names identified | N/A | Class estimates and ownership check |
| **Verified rights and owners** | Renewals and transfers | 🟡 [Sample warning only](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) | 🟡 Same sample | USPTO renewal and assignment records |
| **Commercial context: R&D** | R&D by year, with boundaries stated | ✅ [20 years](../03-market-and-patent-analysis/twenty-years.md) | 🟡 [Latest period](../03-market-and-patent-analysis/market-context-and-peer-selection.md#commercial-context) | Earlier years, and Huawei's report. Not for ranking |
| **Commercial context: AI and cloud** | Sales and orders | 🟡 [Latest quarter](../03-market-and-patent-analysis/market-context-and-peer-selection.md#commercial-context) | 🟡 [Latest period](../03-market-and-patent-analysis/market-context-and-peer-selection.md#commercial-context) | Earlier years, where reported |
| **Maintenance costs** | Fees and renewal behaviour | 🟡 US fees and a [supporting break-even](../04-financial-analysis/us-renewal-break-even.md) | ❌ | Verified rights, renewal rates, and fees for Europe, China and Japan |
| **Findings and recommendations** | Findings tied to decisions | 🟡 [Provisional](../05-findings-and-recommendations/findings.md) | N/A | Depends on everything above |

## What to do, in order

| # | Step | Why | Research action / human review | Cost | Status |
|---|---|---|---|---|---|
| 1 | Preserve the research question, and add the public-data qualification | Everything else depends on it | Researcher decision | None | ✅ |
| 2 | Unify the [technology scope](../01-research-design/scope.md) | Documents disagreed on switching | Researcher decision | None | ✅ |
| 3 | Correct [portfolio terminology](../02-methodology/candidate-portfolio-universe.md#what-each-data-category-establishes) | Counts were being read as ownership | Researcher decision | None | ✅ |
| 4 | Complete classification validation: preliminary software pilot and precision are done. Human hand-labelling of 100 families per primary category (300 total), human–software agreement, repeated-subset consistency and recall are incomplete. [60-publication sheet](../../data/validation/agreement_sheet.csv) | Needed for every comparison | Human hand-labelling, evidence review and adjudication required; software-assisted sampling only | Free, from Google Patents pages | 🟡 |
| 5 | Estimate how much of the universe has been transferred, on a random US sample and USPTO assignment records | [23.5% in my sample](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) | Researcher obtains USPTO records and reviews assignment evidence | Free | ❌ |
| 6 | Run the register spot-check on [35 patents](../../data/validation/spot_check_sample.csv) | Shows the error rate | Researcher checks official registers and reviews all outputs | Free | ❌ |
| 7 | Build comparable portfolios by pool and period, and test H1–H3 | Answers RQ1–RQ3 | Software-assisted processing; researcher validates methods and outputs | Small | ❌ |
| 8 | Re-aim [commercial alignment](../03-market-and-patent-analysis/commercial-alignment.md) to the satcom scope | Feeds RQ3 and RQ4 | Software-assisted processing; researcher validates methods and outputs | None | ❌ |
| 9 | Complete the [Q9 model](../04-financial-analysis/ten-year-maintenance-cost-model.md): USPTO renewal records first, then other offices | Feeds RQ5 | Researcher obtains renewal records and validates model assumptions | Free | ❌ |
| 10 | Pull earlier R&D from competitors' annual reports | Commercial context | Software-assisted extraction; researcher checks source filings | Free | ❌ |
| 11 | Write findings and the executive brief | Answers RQ5 | Researcher writes and approves findings | None | 🟡 |

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

## What can't be answered from public data

| Gap | How the answer handles it |
|---|---|
| Nokia's and competitors' patent budgets | Statutory fee estimates, with assumptions labelled |
| Value of individual patents | Scenarios and indicators, never stated as fact |
| Technical quality of products | Out of scope |
| Current ownership outside the US | Stated as a limit, unless a free source turns up |

## Minimum for a defensible answer

Before 30 November, the essentials are steps 4–7, plus a simple version of steps 9 and 11 using US costs. European, Chinese and Japanese fees can be shown as a stated gap if there's no time.
