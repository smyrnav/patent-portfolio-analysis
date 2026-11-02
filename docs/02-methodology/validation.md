# Validation

**The taxonomy isn't validated.** On preliminary software-generated labels, patent codes failed the precision test in all three categories. Human labelling, human–software agreement and recall haven't been completed. All 421 labels remain a software-generated first pass with `review_status` = `pending`.

## Stages

| Stage | What happens | Size | Pass rule | Status |
|---|---|---|---|---|
| **1. Pilot** | Software-assisted labelling of a sample across all five companies, then rule fixes | 30 per pool | None, rule changes are logged | Preliminary first pass done |
| **2. Freeze** | Lock the rules | N/A | Changes need a logged reason and a re-test | Done, [version 1.1](classification-codebook.md#version-history) |
| **3. Precision** | Software-assisted first-pass labelling of a new random sample per pool, with the codes hidden | 100 per pool | At least 85% | **Preliminary result: failed in every pool** |
| **4. Human validation and agreement** | One human hand-labels sampled families with documented claim evidence, repeats a subset for intra-rater consistency, then compares independent human labels with the first pass | 100 families per primary category; 300 total | Human–software Cohen's kappa of at least 0.7; report intra-rater consistency separately | Not done. [60-publication sheet ready](../../data/validation/agreement_sheet.csv), but the full target isn't met |
| **5. Recall** | Sample related families outside the pools, stratified by company and priority-date period | 100 | Report the miss rate, and adjust if large | Not done |
| **6. Company balance** | Compare precision by company | Across the sample | No company far below the others | Preliminary optical gap found |

The human-validation target uses **family-level sampling**: 100 distinct families per primary category, 300 in total. **Labelling is publication-level**: the human reads the selected publication's claims and records the evidence for each sampled family. This target is separate from the existing software-labelled test slots and doesn't make those first-pass results human-reviewed.

If a label fails, the comparison for that label is reported as low confidence or dropped. Thresholds are my own project standards, not an industry rule.

## Who labelled what

Software assistance produced the first pass on all 421 patents, working from the claims with company, pool, title and codes hidden. I am responsible for the methods, validation, calculations and conclusions, and I haven't yet reviewed these labels. The human review must be completed without reading the corresponding first-pass labels first.

One human annotator can produce human-reviewed labels with documented evidence and repeated-subset intra-rater consistency. Human–software agreement will be reported separately; it isn't inter-human agreement or expert reliability. Cohen's kappa cannot describe agreement between independent humans unless two independent human annotators actually label the sample.

## Files

| File | Contents |
|---|---|
| [`manual_labels.csv`](../../data/validation/manual_labels.csv) | One row per patent: family, applicant, priority date, class, secondary fields, evidence, status, annotator, confidence and version |
| [`validation_slots.csv`](../../data/validation/validation_slots.csv) | Which sample and pool each patent was drawn for |
| [`sample_metadata.csv`](../../data/validation/sample_metadata.csv) | Family ID and priority date from [BigQuery](../../sql/18_validation_sample_metadata.sql), and applicant and current assignee from Google Patents |
| [`agreement_sheet.csv`](../../data/validation/agreement_sheet.csv) | 60 patents for my own labels. `my_label` takes OPT, IPR, DCS, OTHER or MULTI |
| `results_*.csv` | Scores from [`src/score_validation.py`](../../src/score_validation.py) |

[`src/fetch_claims.py`](../../src/fetch_claims.py) and [`src/make_blind_sheet.py`](../../src/make_blind_sheet.py) reproduce the claim download and the blind sheets.

## Pilot result

78 unique patents filled 90 slots. These small, preliminary software-labelled samples only guide the rules.

| Pool | Claims match the class | Main finding |
|---|---|---|
| OPT | 25 of 30 (83%) | 22 of 24 where the patent's first listed code is optical |
| IPR | 14 of 30 (47%) | 13 of the others are OTHER: the code is often secondary |
| DCS | 5 of 30 (17%) | H04L 47 alone: 1 of 19. With H04L 49: 4 of 11 |

## Test design, fixed before reading the test claims

| Item | Decision |
|---|---|
| Sample | 300 slots, 100 per pool, by [random order](../../sql/16_codebook_sample.sql), with pilot patents and one missing page replaced from [spares](../../data/validation/codebook_sample_spares.csv) |
| Company quotas | 40 Nokia, 20 each for Ciena and Cisco, 10 each for Arista and Huawei |
| Extra draw | [100 from H04L 49 only](../../sql/17_codebook_sample_h04l49.sql), because the first switching pool included H04L 47. 32 were already labelled, and 68 were new |
| Subgroups | First listed code in the pool or not, H04L 49 or H04L 47 only, and company |
| Blinding | Company, pool, title and codes hidden, in shuffled order |
| Reading limit | Mostly the start and end of the first independent claim, and the openings of up to two more |

**Not stratified by priority date.** That was added to the method afterwards, so I report [what the sample contains](#precision-by-priority-period) rather than claim it was balanced. The recall sample will be stratified.

## Precision result

343 unique patents filled 400 slots. [Every figure](../../data/validation/results_precision.csv) is recalculated from the labels by the scoring script.

| Pool | What's measured against what | Claims match | 95% range | Pass (85%)? |
|---|---|---:|---|---|
| Optical: H04B 10, H04J 14, H04Q 11/00 | OPT labels out of 100 patents | 73 | 64–81% | No |
| Routing: H04L 45 | IPR labels out of 100 patents | 39 | 30–49% | No |
| Switching as first planned: H04L 49 or H04L 47 | DCS labels out of 100 patents | 21 | 14–30% | No |
| Switching: H04L 49 only | DCS labels out of 100 patents | 42 | 33–52% | No |

H04L 47 alone matched 7 of 70, so switching now uses H04L 49. **Raw code counts can't be used to compare companies.** Any comparison has to use estimates from claims, with ranges and low confidence, as in the [patent landscape](../03-market-and-patent-analysis/patent-landscape.md).

## Confusion between classes

Each row is 100 patents from one retrieval pool, and each column is the class their claims earned. [Source](../../data/validation/results_confusion.csv).

| Pool | OPT | IPR | DCS | OTHER | MULTI |
|---|---:|---:|---:|---:|---:|
| Optical | **73** | 2 | 0 | 23 | 2 |
| Routing | 2 | **39** | 7 | 52 | 0 |
| Switching, H04L 49 or H04L 47 | 1 | 13 | **21** | 65 | 0 |
| Switching, H04L 49 only | 1 | 13 | **42** | 43 | 1 |

Most misses are OTHER, which means the code is listed but the claim is about something else. The only sizeable mix-up between classes is 13 routing claims in the switching pool.

## Records needing review

| Measure | Pilot, of 78 patents | Test, of 343 patents |
|---|---:|---:|
| MULTI | 1 (1.3%) | 3 (0.9%) |
| Low confidence | 6 (7.7%) | 38 (11.1%) |
| MULTI or low confidence | 6 (7.7%) | 39 (11.4%) |
| `review_status` still pending | 78 (100%) | 343 (100%) |

[Source](../../data/validation/results_review_share.csv).

## Human–software agreement

Not measured. [`results_agreement.csv`](../../data/validation/results_agreement.csv) shows 0 of 60 labelled, and the script calculates kappa once all 60 are filled in. The existing sheet and script cover 60 publications; completing them would not satisfy the 300-family human-label target. Any resulting kappa measures human–software agreement, not inter-human or expert reliability.

## Precision by company

Optical precision is 85% for Nokia and 60–70% for the others, on small samples. So raw code counts flatter Nokia against Ciena and Cisco. The other pools show no clear company gap, but samples of 10–20 are too small to rule one out.

## Precision by priority period

[Source](../../data/validation/results_period_balance.csv). Each cell is claims matched out of patents labelled.

| Pool | To 2010 | 2011–2015 | 2016–2020 | 2021 on |
|---|---:|---:|---:|---:|
| Optical | 18 of 19 | 22 of 30 | 24 of 35 | 9 of 16 |
| Routing | 11 of 24 | 13 of 31 | 12 of 34 | 3 of 11 |
| Switching, H04L 49 only | 15 of 29 | 15 of 34 | 10 of 29 | 2 of 8 |

**Precision falls in newer patents in all three pools**, although the newest cells are small. If that holds, trend charts built on code counts would overstate recent activity. So H2 and H3 need claim-based estimates by period, not one precision figure.

## Limits

| Limit | Effect |
|---|---|
| Software-generated first pass, with no human annotation completed | Human hand-labelling, human–software agreement and repeated-subset intra-rater consistency still to run |
| Mostly the start and end of the first claim | Part of why 38 of the 343 labels are low confidence |
| Recall not tested | Estimates only count patents inside a pool, so they could be too low |
| US granted members since November 2006 | Families without a US grant are missing |
| Rule strictness is my own | A looser rule on control-plane claims would raise optical and routing precision |
| Company samples are small | Arista and Huawei have 10 per pool |

## Preliminary boundary check of the draft's 16 examples

I checked all 16 examples from the original draft on Google Patents, under draft 0.1 where REVIEW was still a label. [Each result and link is logged](../../data/validation/draft_examples_check.csv).

| Check | Result |
|---|---|
| Applicant/assignee name matches | 16 of 16 |
| My label agrees | 14 of 16, including the one the draft left as OPT or REVIEW |
| Hedged label resolved | 1: US20250119395A1 is IPR, as its claim is about BGP sessions |
| Disagree | 1: US9866474B2 was REVIEW, as it claims switch management rather than switching |

**These are preliminary boundary tests, not taxonomy validation or expert inter-rater evidence.** It's a small hand-picked set, and 10 of the 16 are Ciena's, 2 each are Nokia's and Cisco's, 1 each are Tigera's and Quanta's, and none are Arista's.

## Is there a ready-made labelled set?

I looked and [found nothing that fits](../appendices/questions.md#q21-has-someone-already-labelled-these-patents-so-i-dont-need-to). Two searches can't prove none exists.
