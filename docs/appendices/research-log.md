# Research log

A record of how this project's method changed, and why. Early decisions keep the wording I used at the time.

## The turning point

I got annoyed with running random queries. Each result suggested another question, and I kept following them without knowing what any of it was for. When "did Nokia move from phones to networks?" came up, I realised the answer was obvious and nobody would decide anything differently because of it, so I stopped and rethought the approach.

## Before and after

| | Before | After |
|---|---|---|
| **Starting point** | Whatever the last result showed | A decision someone has to make |
| **Main question** | What's in this data? | How should Nokia prioritise its patent portfolio investments to support its AI and cloud infrastructure strategy? |
| **Choosing a query** | It seemed interesting | It has to inform a named decision |
| **Unit of analysis** | Mostly owner names and listings | Inventions (patent families) |
| **Data source** | The 2.88 TB table each time | My own 30-year working table |
| **Result** | A trail of facts | Five research questions, ending in investment scenarios and a recommendation |

## What changed along the way

1. **Started with exploration.** I wanted to learn what this work involves, so I began with the question "under which names do Nokia's patents appear?". That taught me how messy the data is, and it was useful as a way to get oriented.
2. **Checked my numbers against each other.** Comparing two totals exposed that my kind code filter had dropped 8,808 older US patents, so I now cross-check totals before trusting them.
3. **Narrowed the scope to 30 years.** That covers everything that could still be alive, plus 10 years of history.
4. **Isolated the data.** Building one working table means later questions don't have to rescan the source table. It used about 289 GB once.
5. **Paused to set a strategy.** I listed what the data can and can't answer, then rebuilt the questions around decisions.
6. **Dropped a query.** I deleted the technology-over-time query before running it, because it only confirmed the obvious on its own.
7. **Raised the questions to business level.** My first list was mostly measures, like when patents expire. I replaced it with five questions a company would actually ask: technology strategy, competitive intelligence, commercial intelligence, portfolio efficiency and market foresight. The earlier measures now sit inside them.
8. **Focused on the role.** The posting has a track for turning patent and financial data into investment decisions, so the project now centres on allocating a limited patent budget. Its outputs are a cost forecast, keep-or-drop analysis, scenarios, sensitivities, a capacity plan and a decision brief. Competitive and licensing questions are parked for now.
9. **Made the work hypothesis-led.** Pulling more metrics wasn't producing answers. I set three priority questions, hypotheses that could be disproved, pass rules for reliability and limits on what gets analysed.
10. **Zoomed in on one question.** After a couple of hours of learning, I'd covered enough to focus on comparing Nokia's patent and investment position with its rivals.
11. **Made the question about investment decisions.** Comparing rivals had become the goal. The earlier question was: *How does Nokia's patent portfolio and associated investment position compare with the leading competitors in AI and cloud infrastructure networking, and what strategic and financial lessons can be identified?* I changed it to: *How should Nokia prioritise its patent portfolio investments to support its AI and cloud infrastructure strategy?* Comparisons and technology labels are now inputs, and I separated what public data can do from what needs internal data.
12. **Tested the technology labels against claims.** All three code pools failed my 85% bar, which [stopped me relying on code counts](../02-methodology/validation.md#precision-result).
13. **Reviewed and consolidated the repository.** See [below](#repository-review-november-2026).

## What I kept from the exploration

The exploration wasn't wasted. It's how I found the messy names, the deal history in the data, the kind code gap and the fields that are too incomplete to rely on. Those findings now shape the strategy.

The [research design](../01-research-design/research-design.md) holds the current plan, including the rule for each new query.

## Repository review, November 2026

I used software assistance for a repository review and checked each recommendation against the files. The review didn't reflect the labelling test, so some of its "to do" items were already done or had changed.

| Recommendation | Decision | Why |
|---|---|---|
| Keep the central question, and add a public-data qualification | Adopted | The objective didn't change |
| Use its wording for the five research questions | Adopted | They connect better. "Validated patent database" is marked as a target, not a claim |
| Formally keep OPT, IPR and DCS | Adopted | Strategy said optical and IP, while the codebook had three |
| `primary_class` with MULTI, plus `review_status` | Adopted as [version 1.1](../02-methodology/classification-codebook.md#version-history) | REVIEW mixed two meanings |
| `manual_labels.csv`, and report confusion, review share and agreement | Adopted | [All built](../02-methodology/validation.md), with agreement pending |
| Stratify the 100-family samples by priority-date period | Partly | The test had already run, so I report the balance. The recall sample will be stratified |
| Rename the portfolio filter, and separate five evidence levels | Adopted | [42 of 179 sampled patents](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) already showed why |
| Make Q9 the principal financial model | Adopted | Break-even stays as support |
| Remove the 1% of licensing sales comparison | Adopted, and extended | I also removed its conclusion that fees look small, and the sales-per-family figure and chart, as they had the same flaw |
| Stop comparing R&D across different boundaries | Adopted | Now shown as context, with Nokia's two boundaries side by side |
| Three maintenance scenarios | Adopted, alongside my three investment strategies | [They answer different questions](../04-financial-analysis/assumptions-and-scenarios.md#scenarios) |
| Monte Carlo only where distributions can be justified | Adopted | The posting's probability curve stays, for inputs with data behind them |
| Target folder structure | Adopted now | It said this could wait, but overlap between documents was the problem I wanted fixed. Where its names conflicted, I used the more specific one |
| `executive-brief.md` | Not created yet | An empty brief would imply a result that doesn't exist |
| Mostly impersonal README | Adopted for the overview | My learning story stays first-person in the logs |
| Config, manifests, shared functions, tests and one workflow | Adopted now | Small to add, and [the tests](../../tests/test_repository.py) keep the docs coherent |

**Corrections found during the review:**

- Several documents said "I labelled" when software assistance made the first pass. They now distinguish software-generated labels from human review.
- The README disclosure understated the software's role. It's now specific.
- The estimates table compared Nokia with other assignees removed against competitors without that adjustment. [Both are now shown on the same basis](../03-market-and-patent-analysis/patent-landscape.md#the-same-estimate-keeping-only-patents-without-another-current-assignee).
- Recalculating from unrounded shares moved four range edges by 1, such as Nokia routing's upper end from 330 to 329.

## Pivot to sovereign satcom, 2 November 2026

The ICEYE–Nokia–Ukraine Letter of Intent (22 October 2026) is the strongest public signal of where Nokia is placing a new bet, so the research question pivots from AI and cloud infrastructure to sovereign satellite communications and defence connectivity. Decision, sources, impact map and execution checklist: [pivot-sovereign-satcom.md](../01-research-design/pivot-sovereign-satcom.md). The pipeline, validation method and cost model carry over; the technology categories, peer set and hypotheses do not.

## Central question rewritten, 2 November 2026

Same day as the pivot decision: adopted the new central question — *Which technological capabilities, patent assets and investment priorities are most important for developing a sovereign LEO satellite communications capability for Ukraine and European government customers?* — and rewrote it in `config/research_parameters.toml`, the README (new title: *Sovereign LEO Communications — Nokia–ICEYE: Technology, Patent Portfolio and Strategic Investment Analysis*), the research design and the five research questions in one pass. H1–H4 are retired in place, T3 in the assumptions register is superseded, and the scope keeps the old categories explicitly marked as the pre-pivot lens pending new satcom code pools. Tests stayed green throughout.

## Deep-research report imported, 2 November 2026

A software-assisted deep-research report on the Ukraine sovereign satcom deal arrived from the Kimi browser version. Imported as [deep-research-ukraine-satcom.md](deep-research-ukraine-satcom.md) with a provenance header: every claim is a source lead, not a project fact. Key claims mined into [sources.md](sources.md#sovereign-satcom-context-post-pivot) with status labels. Its two figures weren't available and its closing editorial line was omitted. Unlike the earlier browser report (AI-RAN/6G drift, rejected), this one is on-scope for the pivot.

## Renamed and made personal, 2 November 2026

Project retitled to *Nokia–ICEYE Sovereign LEO Communications* — the partnership name carries the project better than the generic "Sovereign LEO Communications". The README origin section now records what the pivot actually meant: I'm Ukrainian, the research questions had already moved several times as evidence demanded, and the Ukraine LoI turned a professional exercise into a personal one. Disclosed as motivation, not as evidence.

## Personal position documented, 2 November 2026

The README now states my position plainly: dependence on any foreign private company or foreign administration's politics is itself the vulnerability; Ukraine's communications must be Ukraine's; Finland sheltered me and this project is part of earning my keep. Recorded as motivation, explicitly not as evidence. The language is deliberate — the position is strong, so it doesn't need to be loud; insults would only give a reviewer a reason to discount the analysis.
