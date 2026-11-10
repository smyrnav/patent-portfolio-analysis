# Data quality and lineage

## Where the patent data comes from

1. **Patent offices** publish the records, such as the USPTO, EPO and CNIPA. These are official documents.
2. **Data providers** collect them. The Google table is supplied by [IFI CLAIMS](https://www.ificlaims.com/news/view/blog-posts/public-patent-data-now.htm), and simple families follow the [EPO's DOCDB family identifier](https://inspire.wipo.int/node/3481).
3. **Google** publishes the result in BigQuery. The table was last modified on 23 September 2026, with filings to August 2026. Google's [example code repository was archived in April 2026](https://github.com/google/patents-public-data), so I check the table's own date rather than relying on that repository.
4. **I filter it** with SQL saved in [`sql/`](../../sql/README.md), and the results are saved locally, because sandbox tables expire after 60 days.

The [source manifest](../../data/source_manifest.csv) ties each query to its local snapshot, with a fingerprint that the checks verify.

## How far to trust each part

| Data | Trust | Why |
|---|---|---|
| Publication numbers, offices, filing dates | High | Official bibliographic records |
| Technology codes | **Low for comparing companies** | Examiners' codes, but [claims matched only 39–73% of the time](validation.md#precision-result) |
| US grants | High | US grant dates add up across my queries |
| Grants outside the US | **Low to medium** | Japan shows 0 grant dates, and Austria 99.8% |
| Applicant names | **Medium** | Cleaned names, which keep the filing name after later transfers |
| Legal status and current owner | **Not available in this table** | [IFI sells these separately](https://www.ificlaims.com/news/view/blog-posts/public-patent-data-now.htm) |
| Current assignee on Google Patents | **Medium, sample only** | Google's own computed guess at today's owner — its pages carry a disclaimer that it may be inaccurate. Good enough to flag "this patent may have changed hands", not good enough to state who legally owns it; the official record is the patent office's assignment register (USPTO for US patents), not yet checked |
| Family counts | Medium | [Providers define families differently](https://iamip.com/wiki/patent-family/) |

I didn't find a formal accuracy audit of this dataset.

## How I check it

| Check | Status |
|---|---|
| **Compare totals across queries.** That's how I found the 8,808 missing US patents | Done, and [automated](../../src/check_outputs.py) where possible |
| **Spot-check against official registers.** Compare [a repeatable random sample of 35](../../data/validation/spot_check_sample.csv) with [Espacenet](https://worldwide.espacenet.com/) and the USPTO, and record the error rate. It has none from Japan, as no Japanese grants were detected | Not done |
| **Compare with what Nokia reports.** [New families follow its reported new inventions](../03-market-and-patent-analysis/twenty-years.md#my-family-counts-follow-nokias-own-numbers), though its counting rules may differ | Done |
| **Check patents against the inventor's own words.** Read the numbered sentences at the back of sampled patents and mark each bucket right or wrong. See [validation](validation.md) | Precision done, agreement and recall not done |
| **Keep the docs coherent.** [Automated tests](../../tests/test_repository.py) check links, shared wording and label files | Done |

## Where to find financial data

| Source | What it gives | Status |
|---|---|---|
| [Nokia's 20 annual reports, FY2006–FY2025](../../data/raw/annual_reports_manifest.csv) | R&D, licensing, segments, deals and risks | Official, [key figures extracted](../03-market-and-patent-analysis/twenty-years.md) |
| [Nokia's Q3 2026 report](https://www.sec.gov/Archives/edgar/data/924613/000110465926117972/tm2628115d1_6k.htm) | Technology Standards net sales of €425M in Q3 and €1,217M for January–September, and R&D expenses of €1,251M in Q3 | Official |
| [USPTO fee schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule) | US renewal fees | Official |
| [EPO fee rules](https://www.epo.org/en/legal/epc/2020/EPC_rfees_20260401_en_20260326.pdf) | European fees from 1 April 2026 | Official, figures not extracted yet |
| National patent offices | Renewals after a European grant, by country | Official, not collected yet |
| [OPPO v. Nokia ruling](https://www.chinaiplawupdate.com/2023/12/chongqing-no-1-intermediate-peoples-court-sets-global-frand-rate-for-5g-seps-at-0-707-unit-in-nokia-oppo-case/) | A court's 5G rates of $1.151 and $0.707 per phone, by territory | Disputed by Nokia and later settled confidentially |
| [USPTO assignment data](https://iipla.org/news/uspto-to-upgrade-assignment-search-and-relocate-patent-export-data-to-open-data-portal-in-july-2026) | US patent sales and transfers | Public, location to be confirmed |

Nokia's actual patent budget, its costs per patent and the terms of its deals remain private, so those stay as labelled assumptions.
