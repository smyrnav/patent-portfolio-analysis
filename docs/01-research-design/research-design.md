# Research design

This is the authoritative protocol for the project. The [scope](scope.md) and [research questions](research-questions.md) sit beside it, and progress is tracked only in the [evidence tracker](../appendices/evidence-gaps.md).

## Central research question

> **What does publicly available patent data reveal about the satellite-communications patent portfolios of Nokia, ICEYE and selected competitors, and how reliable are those comparisons?**

Adopted 24 November 2026, after a factual audit of the repository. This is the fourth wording. The earlier versions asked which capabilities and investment priorities mattered most, then what the partners could reuse, develop or acquire. Both promised more than public records can show: patent data cannot establish whether a company can reuse an invention, whether it has the engineering to implement it, what licences it already holds, or what the partnership agreed internally. The current question asks only what the data can answer, plus how much the answers can be trusted. History is in the [research log](../appendices/research-log.md).

## What the project is

An independent, outside-in look at public patent records in the context of the Nokia–ICEYE sovereign LEO satellite communications partnership (announced October 2026, with a Letter of Intent to Ukraine's Ministry of Defence).

The core work:

- Collect patent records from Google Patents' public BigQuery dataset.
- Identify company applicants and their historical names.
- Group publications of the same invention into patent families.
- Find candidate satellite-communications patents with CPC classification codes.
- Check whether those candidates are genuinely relevant by reading patent claims.
- Compare company portfolios only when the classification proves reliable enough.

## Two workstreams, one subject

| | Patent research | Procurement research |
|---|---|---|
| Question | What does patent data show about the companies' portfolios, and how reliable is it? | What do Ukrainian public procurement records show about government purchases and planned purchases of satellite-related equipment and services? |
| Data | Google Patents public dataset (BigQuery) | Prozorro portal search API |
| What it measures | Disclosed inventions and applicants | Public purchasing activity |
| What it cannot measure | Operational capability, licences, internal deals | The whole market (classified and non-public buying are invisible); amounts actually paid |

The two are complementary. Neither independently establishes technical capability.

## Evidence boundaries

This project is not a freedom-to-operate assessment, not an engineering evaluation, and not an investment recommendation. It has no access to internal company data. Findings come in three kinds, labelled as such: observations (what the data shows), hypotheses (what might explain it) and conclusions (what survives validation).

Three number types are never treated as interchangeable:

1. **Total company patent families** in the dataset (name matching, no technology filter — e.g. [query 24](../../sql/24_satcom_peers_30y.sql)).
2. **Candidate satcom families** returned by CPC code searches ([query 32](../../sql/32_pool_census.sql)) — unvalidated by definition.
3. **Confirmed relevant families** after claims review — none exist yet; human validation is not done.

## Reliability checks

Every comparative claim must pass these before it is stated as established.

| Check | Pass rule | Status |
|---|---|---|
| **Classification** | At least 85% precision per label on human-reviewed labels, kappa of at least 0.7, recall reported | Failed the 13 November re-test (70.8% agreement with software first-pass labels — a diagnostic, not validated accuracy). Redesign next |
| **Applicant matching** | Top names reviewed per company, register spot-check | Satcom names reviewed except [11 flagged names](../../data/interim/satcom_name_review.csv); spot-check not done |
| **Ownership** | Current owner from assignment or register evidence | Not done; [early warning](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) |
| **Time** | 2020–2024 main period; 2025–2026 provisional | Rule set |

The 85% bar and the kappa threshold are this project's own acceptance rules, not industry standards.

## How to state an answer

1. **Answer:** one sentence
2. **Evidence:** the numbers and sources
3. **Confidence:** high, medium or low, with the reason
4. **What would change it:** the result or data that would overturn it
5. **Decision:** what to do, investigate or stop doing

## Rules that stop endless metric-pulling

- A query runs only if it feeds a stated question, with the deciding result written down in advance.
- "The data can't answer this" is a valid result.
- Statistical tests run only on validated data, per the [hypothesis rules](satcom-hypotheses.md).
- When more data wouldn't change the decision, the analysis stops.

## Where each part lives

| Part | Document |
|---|---|
| Technology, companies, offices and dates | [Scope](scope.md) |
| Research questions | [Research questions](research-questions.md) |
| Candidate CPC pools | [Satcom code pools](satcom-code-pools.md) |
| Labelling rules | [Classification codebook](../02-methodology/classification-codebook.md) |
| Whether the labels can be trusted | [Satcom validation plan](../02-methodology/satcom-validation-plan.md) |
| What the counts do and don't establish | [Candidate portfolio universe](../02-methodology/candidate-portfolio-universe.md) |
| Procurement workstream | [Procurement demand](procurement-demand.md) |
| Results so far | [Findings](../05-findings-and-recommendations/findings.md) |
| Pre-pivot and parked work | [Archive](../../archive/) |
