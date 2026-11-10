# Satcom validation plan

**Status: draft, 8 November 2026.** Companion to [satcom-code-pools.md](../01-research-design/satcom-code-pools.md). This plans how the five candidate pools (SAT, ISL, GRD, NET, SEC) earn the right to be used in comparisons. Nothing is validated yet, and per the [pivot rule](../01-research-design/pivot-sovereign-satcom.md), nothing carries over from the pre-pivot categories.

## What a validation check actually is

The pools sort patents automatically, using the patent office's category labels. Those labels are wrong surprisingly often, so before any bucket is trusted, a human checks the machine's work on a sample. The check runs at two levels:

**One patent.** The machine says "this patent is satellite-communications payload technology." A human opens the patent, reads the numbered sentences at the back where the inventor states what they invented, and gives their own verdict: yes it is / no it isn't. The human's reading is the reference we treat as reality. Example from this project: an ICEYE patent titled "Antenna and antenna array" sounds communications-relevant, but its numbered sentences claim a synthetic-aperture-radar imaging system — it images, it does not communicate. Machine wrong, human catches it.

**One bucket.** One patent tells us nothing; the bucket is judged on a random sample (30–100 patents). **Precision = how often the machine was right = right ÷ total.** The bucket passes only if at least 85 out of every 100 sampled patents genuinely belong in it, per the human who checked. The opposite question gets checked too: we sample patents the buckets did *not* catch — from the related categories we deliberately left out — and count how many turn out to be real satcom patents we are missing entirely (**recall**). A bucket can pass 85% and still catch only a tenth of what exists: clean but blind. If the miss rate is large, the bucket gets widened and re-tested.

Three protections keep the human verdict honest: the question is narrow ("do these numbered sentences describe technology for capability X?"), every verdict gets a written reason a third party can audit, and some patents get labelled twice to measure whether the human agrees with themselves. If the human is inconsistent, the 85% number means nothing and the question gets tightened first.

When a bucket fails, we diagnose which patents it wrongly catches, fix the code pool, and re-test — iterating until it clears the bar. The rest of this document is the mechanics of that loop.

## Why a new validation, and what the last one taught

The pre-pivot pools failed the 85% precision bar in all three categories ([full record](validation.md#precision-result)). That failure is useful: it tells us where the new pools will break if we repeat the design.

| Lesson from the pre-pivot failure | What changes in the satcom plan |
|---|---|
| Most misses were OTHER: the code was listed, but the claims were about something else | Report precision split by **first-listed code vs. secondary code** from the start, not as an afterthought (pre-pivot optical: 22 of 24 matched when the first code was optical) |
| Precision fell in newer patents in all three pools | **Stratify every sample by priority period from the start.** The pre-pivot sample wasn't stratified, and the imbalance had to be reported after the fact |
| Optical precision was 85% for Nokia but 60–70% for competitors — raw counts flattered Nokia | **Per-company quotas and a company-balance check**, with samples large enough to see a gap |
| Broad codes failed badly (H04L 47: 7 of 70 alone) | Pools stay narrow; the pilot tests each code separately before any pooling |
| The 300-family human-labelling target was never completed — human time is the bottleneck | The human stage is **staged by pool priority** (below), with the effort stated honestly |

## Predictions, logged in advance

Logging expectations before touching data keeps the validation honest — a surprise is allowed, a retrofitted explanation is not.

- **SAT, ISL, GRD** should behave like pre-pivot optical: specific hardware codes, decent first-code precision. Expected to pass or come close.
- **SEC** is the likely failure, same shape as pre-pivot routing: security codes like H04K 1/00 attach as secondary codes to ordinary communications patents. If it fails, the fix to test is restricting to the satellite-specific access-prevention codes (H04B 7/18565, H04B 7/18593), not loosening the claim rules.
- **NET** is the other risk: H04W 84/06 describes where a network runs, not what the invention does, so it may attach to any wireless patent. Watch it in the pilot.
- **ISL may be too small to sample.** Inter-satellite-link patents are rare. A pool too small for 100 samples is a finding about the field, not a validation failure — report the census count as-is.

## Stages

Adapted from the [six-stage design](validation.md#stages), with one stage added at the front.

| Stage | What happens | Size | Pass rule |
|---|---|---|---|
| **0. Pool census** | Count candidate families per pool, company and priority period in BigQuery, before any sampling | Full counts | None — this sizes everything below and shows early whether ICEYE's record is comms-thin |
| **1. Pilot** | Software-assisted labelling, blind (company, pool, title and codes hidden), then rule fixes with logged reasons | 30 per pool, each code reported separately | None; rules change here, not later |
| **2. Freeze** | Lock the satcom codebook as version 1.0 | N/A | Later changes need a logged reason and a re-test |
| **3. Precision** | New random sample per pool, codes hidden, **stratified by priority period and company** | Up to 100 per pool; fewer where the census is smaller, reported as-is | At least 85% per pool |
| **4. Human validation** | Hand-labelling with documented claim evidence, a repeated subset for intra-rater consistency, then human–software agreement (Cohen's kappa) | Staged by pool priority (below) | Kappa of at least 0.7; intra-rater reported separately |
| **5. Recall** | Sample related families outside the pools, stratified by company and period | 100 | Report the miss rate; adjust pools if large |
| **6. Company balance** | Compare precision by company | Across the sample | No company far below the others |

## The human-labelling problem, stated plainly

The pre-pivot target was 100 families per category, 300 in total, and it was never finished — that is the main reason the old comparison stayed "first estimates". Five pools at the same rule would mean 500. That is not realistic before the application deadline, so this plan needs a **researcher decision** between two honest options:

| Option | Consequence |
|---|---|
| **A. Stage by decision relevance** — hand-label the pools in the order the answer needs them (likely SAT and SEC first: what Nokia has, and whether it's protected) | Later pools stay software-first-pass and are reported as such |
| **B. Smaller human samples per pool** — for example 60 per pool | Wider ranges on every precision figure; all comparisons labelled low confidence |

Either is defensible if stated. What isn't defensible is a third option: presenting software-generated first-pass labels as if they were validated. The pre-pivot docs hold that line, and the satcom work holds it too.

## What happens when a pool fails

Same rule as before: the comparison for that pool is reported as low confidence or dropped. A failed pool is not hidden and not re-labelled until it passes — rule changes happen in the pilot, with logged reasons, or not at all.

## Files and tooling

Reuse, don't rebuild: [`src/fetch_claims.py`](../../src/fetch_claims.py), [`src/make_blind_sheet.py`](../../src/make_blind_sheet.py) and [`src/score_validation.py`](../../src/score_validation.py) work unchanged. New files get a satcom prefix (`data/validation/satcom_…`) so the pre-pivot record stays untouched. The new label set (SAT, ISL, GRD, NET, SEC, OTHER, MULTI) enters [`config/research_parameters.toml`](../../config/research_parameters.toml) only when the pools are accepted — one pass, keeping the consistency tests green.
