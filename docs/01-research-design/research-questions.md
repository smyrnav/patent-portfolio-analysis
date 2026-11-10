# Research questions

Five questions support the [central research question](research-design.md#central-research-question). Each one feeds the next: reuse, exposure, advantage, action, then priorities. Every question names its query or desk-research task and the measurable output it produces. Re-aimed to sovereign LEO satellite communications in the [2 November 2026 pivot](pivot-sovereign-satcom.md); rebuilt 9 November 2026 around the build–buy–partner–license framing.

| # | Research question | How it's answered | Measurable output | Limit |
|---|---|---|---|---|
| **RQ1** | Which technologies the system needs are already covered by Nokia's or ICEYE's existing patents — where can the partnership reuse instead of develop? | Census and validated labels on the Nokia-lineage and ICEYE tables against the [five pools](satcom-code-pools.md) | Reusable-asset inventory per pool, with 95% ranges from measured precision | Coverage isn't freedom to operate; owner data starts US-only |
| **RQ2** | Where do third parties hold significant positions in those same technologies — where could licensing costs, freedom-to-operate constraints or competitor dependence bite? | Third-party pool counts (name research first, then the new peers table), then [H1's chi-square](satcom-hypotheses.md) on precision-adjusted counts | Exposure list per pool, with χ², Cramér's V and residuals | A big count flags where to investigate, nothing more. Whether one patent can actually block the system depends on whether its numbered sentences cover exactly what we want to build — a case-by-case legal judgment this project doesn't make (glossary: [freedom to operate](../glossary.md)) |
| **RQ3** | Where is competitor patenting rising, and where could the partnership build defensible IP that is hard to replicate? | Priority-year trends per pool (H2); citation context (H3) | Differentiation map: crowded areas versus open ones | Publication lag blurs the newest years |
| **RQ4** | For each required capability, what does the evidence support: build, buy, partner or license? | RQ1–RQ3 evidence mapped onto the six capabilities; desk research on licensing and acquisition precedents | Capability × action matrix, each cell linked to its evidence | Public data can't show internal costs or existing licences |
| **RQ5** | Which R&D investments are urgent, which can wait, and which aren't justified? | Score pools on reuse, exposure, growth and cost against published weights, then a sensitivity check on the weights | Ranked priorities, with the ranking's sensitivity shown | Priorities to investigate, not decisions |

Current status is in the [evidence tracker](../appendices/evidence-gaps.md). The patent database isn't validated yet, so every output above arrives with its confidence label attached.

**Q9 sits under RQ5.** "What would it cost to maintain a defined portfolio of patent rights over ten years, as a range?" is the [main financial workstream](../04-financial-analysis/ten-year-maintenance-cost-model.md), and its cost range feeds the priorities ranking.

## The management decisions these serve

Each research question exists to serve one decision. If an answer wouldn't change the decision, it doesn't belong in the findings.

| Research question | Management decision | Useful output |
|---|---|---|
| RQ1 | Accelerate development | Existing technology that can be leveraged |
| RQ2 | Protect commercialisation | Potential IP conflicts and licensing dependencies |
| RQ3 | Differentiate the product | Opportunities for defensible technological advantages |
| RQ4 | Allocate R&D resources | Build, buy, partner or license recommendations |
| RQ5 | Prioritise investment | Ranked technology investment opportunities |

**Caveat.** Patent data alone cannot establish freedom to operate, engineering readiness, actual development costs or market demand — those need other evidence. What patent intelligence can do is identify where management should investigate before committing resources.

## Hypotheses

**H1–H4 below are retired.** They belong to the pre-pivot optical/routing/switching scope. The new satcom hypotheses are drafted in [satcom-hypotheses.md](satcom-hypotheses.md), gated by the [validation plan](../02-methodology/satcom-validation-plan.md). The retired set is kept here for the record.

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

Patents show technical position, not product quality or market share. Citations and family counts are indicators rather than value. A final R&D or licensing decision also needs Nokia's internal costs, roadmaps and deals.
