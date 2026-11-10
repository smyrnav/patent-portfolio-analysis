# Explain it yourself

A checklist of the numbers and ideas I should be able to explain without notes.

## Numbers to work through

| Claim | Calculation | Where it comes from |
|---|---|---|
| About 2.9 applications per invention | 212,660 ÷ 72,207 = 2.95 | [Table check](../../data/raw/portfolio_30y_check.csv) |
| About 4 publications per invention | 289,998 ÷ 72,207 = 4.02, as one application can be published more than once | [Table check](../../data/raw/portfolio_30y_check.csv) |
| Distinct Alcatel/Lucent share: not available | Origin counts overlap, so neither (9,607 + 7,249) ÷ 36,866 nor (9,607 + 7,249) ÷ 36,630 is valid. The distinct union awaits a corrected publication-level SQL rerun | [US recount](../../data/processed/us_30y_recount.csv) |
| 36,630 publications and 37,710 listings | The saved data verify distinct US publications and owner-publication listings; the overlapping origin counts sum to 36,866 | [US recount](../../data/processed/us_30y_recount.csv) |
| Top 10 names account for 93% of listings, not unique patents or current ownership | 35,124 ÷ 37,710 = 93.1% of owner-publication listings | [US recount](../../data/processed/us_30y_recount.csv) |
| 23.5% show another assignee | 42 ÷ 179 unique sampled Nokia-lineage patents | [Current assignee check](../../data/validation/results_current_assignee.csv) |
| Optical pool precision of 73% | 73 of 100 sampled patents earned OPT from their claims, with a 95% range of 64–81% | [Precision results](../../data/validation/results_precision.csv) |
| 8,808 patents were missed | Count of kind code A in the check | [Kind codes](../../data/raw/us_kind_codes.csv) |
| Europe is 79% of the US | 44,353 ÷ 56,039 = 79.1% | [Filings by office](../../data/raw/filings_by_country.csv) |

## Questions to be ready for

1. **Why count patent families?** One invention filed in many countries would otherwise look like many inventions.
2. **What went wrong with the first search?** Filtering on kind code B dropped older US patents that use kind code A. A second query's higher total exposed it.
3. **Why use filing date?** A US patent generally runs 20 years from filing, so filing date best shows what could still be alive.
4. **Why is there no distinct Alcatel/Lucent share?** A publication can appear under more than one origin, so adding the overlapping origin counts cannot produce a distinct-publication share. The saved CSV doesn't contain the publication-level union needed to correct it.
5. **Why did you remove the 1% of licensing sales figure?** Sales depend on far more than fees, so that ratio doesn't establish financial efficiency.
6. **Why not rank patents by revenue?** Public data doesn't show revenue per patent or licensing terms.
7. **Why did you stop exploring?** The queries weren't tied to a decision, so I rebuilt the work around decisions.
8. **What's the biggest weakness?** Current ownership and legal status aren't verified, so the counts describe a [candidate universe](../02-methodology/candidate-portfolio-universe.md), not Nokia's portfolio.
9. **What is a validation check, concretely?** The machine sorts patents into buckets using the patent office's labels; a human reads the numbered sentences at the back of a random sample and marks the machine right or wrong. A bucket is trusted only when at least 85 of 100 checks come out right.
10. **Why doesn't SpaceX dominate your numbers?** It holds 110 patent families against Airbus's 19,488 — a trade-secret strategy, not a technology gap. Patent counts measure published IP, so the strongest player is nearly invisible, and the analysis says so.
11. **Could Ukraine supply its own satcom technology?** Not from patents: no Ukrainian corporate satcom patent base exists (16 individual inventors, one family each), and foreign owners have filed only 16 satcom families at the Ukrainian office, ever. The system's technology will be foreign-patented, which is what makes licensing and partnership central.
12. **How do you know a company name is really that company?** A census of every name variant first, then a written keep/drop/review decision per name. That is how an LED manufacturer was caught under "Airbus" and a Brazilian first name under "Thales".

## Read in the PATSTAT catalog

Page numbers are from the autumn 2026 PDF.

| Topic | Page |
|---|---|
| Harmonised names and where they come from | 21 |
| `TLS201_APPLN`: applications | 46 |
| `TLS206_PERSON`: applicants and inventors | 54 |
| `TLS225_DOCDB_FAM_CPC`: technology codes by family | 74 |
| `TLS231_INPADOC_LEGAL_EVENT`: legal events | 83–84 |
| `TLS803_LEGAL_EVENT_CODE`: legal event codes | 88 |
| `FEE_RENEWAL_YEAR` | 179 |
| `LAPSE_DATE` | 208 |

## Do it myself

- [x] Rerun [the recount](../../sql/08_recount_us_30y.sql) and match the totals. All 24 rows matched on 31 October 2026, on the same working table
- [ ] Open the table and read 10 rows, including their applicant/assignee names and technology codes
- [ ] Read the catalog pages above
- [ ] Explain why the overlapping origin counts cannot produce a distinct Alcatel/Lucent share
