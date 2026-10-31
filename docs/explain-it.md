# Explain it yourself

A checklist of the numbers and ideas I should be able to explain without notes.

## Numbers to work through

| Claim | Calculation | Where it comes from |
|---|---|---|
| About 2.9 applications per invention | 212,660 ÷ 72,207 = 2.95 | [Table check](../data/raw/portfolio_30y_check.csv) |
| About 4 publications per invention | 289,998 ÷ 72,207 = 4.02, as one application can be published more than once | [Table check](../data/raw/portfolio_30y_check.csv) |
| 46% carry an Alcatel or Lucent name | (9,607 + 7,249) ÷ 36,866 = 45.7% | [US recount](../data/processed/us_30y_recount.csv) |
| 36,866 versus 36,630 | Origins add up to more than the unique patents, as a patent can sit under two origins | [US recount](../data/processed/us_30y_recount.csv) |
| Top 10 names hold 93% of listings | 35,124 ÷ 37,710 = 93.1% | [US recount](../data/processed/us_30y_recount.csv) |
| 8,808 patents were missed | Count of kind code A in the check | [Kind codes](../data/raw/us_kind_codes.csv) |
| Europe is 79% of the US | 44,353 ÷ 56,039 = 79.1% | [Filings by office](../data/raw/filings_by_country.csv) |

## Questions to be ready for

1. **Why count patent families?** One invention filed in many countries would otherwise look like many inventions.
2. **What went wrong with the first search?** Filtering on kind code B dropped older US patents that use kind code A. A second query's higher total exposed it.
3. **Why use filing date?** A US patent generally runs 20 years from filing, so filing date best shows what could still be alive.
4. **Does 46% mean Nokia owns those patents?** No. It's the name on the patent, and some may have been sold or transferred.
5. **Why not rank patents by revenue?** Public data doesn't show revenue per patent or licensing terms.
6. **Why did you stop exploring?** The queries weren't tied to a decision, so I rebuilt the work around decisions.
7. **What's the biggest weakness?** Current ownership and legal status aren't known yet, so the findings describe a historical portfolio.

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

- [x] Rerun [the recount](../sql/08_recount_us_30y.sql) and match the totals. All 24 rows matched on 31 October 2026, on the same working table
- [ ] Open the table and read 10 rows, including their owners and technology codes
- [ ] Read the catalog pages above
- [ ] Explain the 46% figure and its limits out loud
