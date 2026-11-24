# Research questions

Three questions support the [central research question](research-design.md#central-research-question). Rebuilt 24 November 2026: the previous five-question structure — reuse, exposure, advantage, build–buy–partner–license, then ranked investment priorities — was retired because RQ4 and RQ5 promised conclusions public data cannot deliver, and all five depended on a classification that [failed validation](../02-methodology/satcom-validation-plan.md) on 13 November. The retired structure is summarised [below](#retired-questions); the satcom hypotheses that survive are in [satcom-hypotheses.md](satcom-hypotheses.md), gated by the validation plan.

| # | Research question | How it's answered | Output | Limit |
|---|---|---|---|---|
| **RQ1** | What technological capabilities does a sovereign LEO communications system need, and what is each partner demonstrably contributing? | Desk research on the partnership's public disclosures and product documentation, plus [procurement records](procurement-demand.md) showing what governments actually buy, mapped onto the system components (space segment, ground segment, terminals, network integration, security) | Capability map: what the system needs, what buyers demonstrably pay for, who contributes what, and what remains undisclosed | Public descriptions and tenders only. The actual division of engineering work and IP ownership between Nokia and ICEYE is not disclosed, so undisclosed stays undisclosed |
| **RQ2** | What relevant patent assets are publicly observable across Nokia, ICEYE and the selected competitors? | Census and validated labels on the Nokia-lineage and [peers](../../sql/24_satcom_peers_30y.sql) tables against the [satcom pools](satcom-code-pools.md) | Validated patent landscape per pool, with 95% ranges from measured precision | Nothing comparative ships until a pool passes the 85% precision bar. Holding a patent doesn't mean the partnership may build it, and current ownership is unverified outside early US checks |
| **RQ3** | Where are the significant third-party IP concentrations, evidence gaps and uncertainties that warrant further investigation? | Third-party pool counts (after RQ2 validation), [H1–H3](satcom-hypotheses.md) on precision-adjusted counts, plus the [evidence-gap tracker](../appendices/evidence-gaps.md) | Due-diligence priority matrix: where to look, why, and at what confidence | A big third-party count flags where to investigate, nothing more. Whether one patent can block the system is a case-by-case legal judgment this project doesn't make (glossary: [freedom to operate](../glossary.md)) |

Current status is in the [evidence tracker](../appendices/evidence-gaps.md). The patent classification isn't validated yet, so every output above arrives with its confidence label attached.

## The decisions these serve

Each research question exists to serve one decision. If an answer wouldn't change the decision, it doesn't belong in the findings.

| Research question | Decision it supports | Useful output |
|---|---|---|
| RQ1 | Understand what is being built | A shared, sourced picture of the system and the partners' roles |
| RQ2 | Reuse what exists | An inventory of observable partner and competitor assets, trusted at a measured level |
| RQ3 | Investigate before committing | A prioritised list of dependencies, gaps and uncertainties for internal technical and legal review |

The endpoint is a due-diligence agenda for Nokia's portfolio and strategy teams — not a build/buy/license verdict and not a ranked R&D budget. Those need internal costs, existing licences and engineering judgment that public data doesn't contain.

## The validation gate

No comparative claim between companies may use a pool that hasn't passed the [85% precision bar](../02-methodology/satcom-validation-plan.md) with human-reviewed labels. The 13 November re-test measured 70.8% against first-pass reference labels, so every company comparison currently waits for test #3: a redesigned taxonomy (separating primary capability from technology attributes such as inter-satellite links), a new stratified sample, human review, and re-measured precision and recall. Discovering the instrument was unreliable is a result; acting as if it weren't would be an error.

## Retired questions

Kept for the record; they return only if the three questions above are answered and a business need justifies them.

| # | Retired question | Why retired |
|---|---|---|
| Old RQ4 | For each required capability: build, buy, partner or license? | Presumes freedom-to-operate and cost evidence public data can't supply. The Ukraine domestic-base part survived and is answered: no Ukrainian corporate satcom patent base exists, so domestic sourcing is not an option ([finding S1](../05-findings-and-recommendations/findings.md)) |
| Old RQ5 | Which R&D investments are urgent, which can wait, which aren't justified? | Ranking a company's internal R&D spend from outside was never supportable. RQ3's due-diligence priorities replace it |
| Q9 cost model | Ten-year maintenance cost range for a defined portfolio | Parked with the rest of the [financial analysis](../../archive/parked-financial-analysis/) as a separate methodology exercise; it fed old RQ5 |

## Hypotheses

**H1–H4 below are retired.** They belong to the pre-pivot optical/routing/switching scope. The current satcom hypotheses are drafted in [satcom-hypotheses.md](satcom-hypotheses.md), gated by the [validation plan](../02-methodology/satcom-validation-plan.md). The retired set is kept here for the record.

| # | Hypothesis (retired) | Feeds | Measure | What would disprove it |
|---|---|---|---|---|
| **H1** | Infinera materially strengthened Nokia's optical position | RQ1, RQ2 | Optical families and share, with and without Infinera | Infinera adds little in key optical areas, or mostly duplicates Nokia's cover |
| **H2** | Nokia's position trails the leaders in IP routing and data-centre switching | RQ2 | Share of new families in routing and switching, 2020–2024 | Nokia's share is level with or above the leaders' |
| **H3** | Part of Nokia's cover is ageing without enough replacement | RQ1, RQ5 | Families reaching 20 years by 2036, against new families | New families outnumber expiring ones in each category |
| **H4** | Cover in the main markets has gaps | RQ1, RQ2, RQ4 | Share of families in the US, Europe, China and Japan, against peers | Coverage matches peers' in each market |

**Output for H1–H4:** a heatmap of the three categories against the five companies, showing share and growth, then a short list of gaps ranked by size, confidence and link to the business.

## Parked extensions

These only start if the main question is answered. See [scope](scope.md#parked).

| # | Hypothesis | Measure | What would disprove it |
|---|---|---|---|
| H5 | Nokia has a leading position in RAN automation | Share of families matched to a tested definition | Share isn't in the top group |
| H6 | Partners hold important capabilities Nokia lacks | Comparison of technology areas across partners | Partner areas mostly overlap with Nokia's |
| H7 | Multimedia and non-smartphone areas have room to grow in licensing | Declared and multimedia families, against public deal coverage | Public sources show those markets are already widely licensed |
| H8 | Nokia's declared families have long enough life to support licensing | Remaining years by standard | Most declared families expire soon |

A licensing database could contain the company, sector, relevant standards, public evidence of use, known licence status, source link and date. It couldn't contain confidential terms, or a claim that a company infringes or needs a licence. "No public licence found" doesn't mean unlicensed.

## What public data can't settle

Patents show technical position, not product quality or market share. Citations and family counts are indicators rather than value. The partnership's internal division of work, existing licences, engineering readiness and development costs are invisible from outside. A final R&D or licensing decision also needs Nokia's internal costs, roadmaps and deals.
