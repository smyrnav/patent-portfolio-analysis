# Technology classification codebook

Version 0.1, a draft to be frozen before any patent comparison. It defines what counts as optical, IP routing or data centre switching, so comparisons with rivals aren't caused by inconsistent labels.

Its starting point was a draft from another AI tool. The changes I made are [listed below](#what-i-changed-from-the-draft).

## The labels

| Label | What the invention mainly does | Maps to Nokia unit | CPC codes used to find candidates |
|---|---|---|---|
| **OPT:** Optical networking | Transmits, receives, multiplexes or switches optical signals | Optical Networks | H04B 10, H04J 14, optical parts of H04Q 11 |
| **IPR:** IP routing | Calculates, selects, maintains or distributes packet routes | IP Networks | H04L 45 |
| **DCS:** Data centre switching | Switches packets, or manages fabrics, queues and congestion in data centre networks | IP Networks | H04L 49, selected H04L 47 |
| **OTHER** | None of the above | N/A | N/A |
| **REVIEW** | Two labels can't be separated from the claims | N/A | N/A |

CPC codes only find candidates, and they don't decide the label. H04L 47 is broad traffic control, and H04L 12 and G02B 6 are too broad to use without another signal.

## Decision rules

Read the independent claims first, then the abstract and description for context. Titles and CPC codes aren't evidence.

| Rule | If the main contribution is about | Label |
|---|---|---|
| 1 | Optical signals, components, wavelengths or photonic switching | OPT |
| 2 | Where a packet should go, or how routes are calculated and shared | IPR |
| 3 | Switch devices, fabrics, queues, buffers, scheduling or fabric topology | DCS |
| 4 | None of these | OTHER |
| 5 | Two labels that truly can't be separated | REVIEW |

Where a patent is used doesn't set its label. A routing patent for data centres is still IPR.

## Extra fields

| Field | Values | Why |
|---|---|---|
| `dc_context` | 0 or 1 | Explicitly for data centres, HPC or cloud |
| `optical_medium` | 0 or 1 | Depends on optical transmission |
| `ai_cloud_relevance` | 0 none, 1 possible, 2 explicit | Stops a general networking patent counting as an AI patent |
| `evidence` | Short quote or claim number | Makes each label checkable |
| `confidence` | High, medium or low | Shows which labels are weak |

## Testing the definitions

| Stage | What happens | Size | Pass rule |
|---|---|---|---|
| **1. Pilot** | Label a sample across Nokia and each core rival, then fix the rules | 30 families per label | No pass rule, rule changes are logged |
| **2. Freeze** | Lock version 1.0 | N/A | No more changes without a logged reason and a re-test |
| **3. Precision** | Label a new random sample per pool, with the codes hidden | 100 families per label | At least 85% precise, reported with a range of about ±7 points |
| **4. Agreement** | I independently label 60 of those families, 20 per label, and compare | 60 families | Cohen's kappa of at least 0.7 |
| **5. Recall** | Sample related families outside the pools, to see what the codes miss | 100 families | Report the miss rate, and adjust if large |
| **6. Company balance** | Compare precision by company | Across the sample | No company is far below the others |

If a label fails, the comparison for that label is reported as low confidence or dropped.

**Who labels:** Claude does the first pass as a tool, and I label the 60 independently and settle disagreements. AI and human agreement doesn't equal two human experts, and the repo will say so.

**Thresholds:** these are my own project standards, not an industry rule.

## Data for labelling

| Data | Source | Status |
|---|---|---|
| Family, dates, codes, titles and abstracts | [My working table](../sql/06_create_portfolio_30y.sql) for Nokia, and a rival table to build | Nokia ready |
| Claims | Google table, at 118.95 GB for the claims column, or Google Patents pages for the sample only | Not collected |
| Date for trends | Earliest `priority_date` in each family | Field available |

Google's table has US full text, while [other offices may only have bibliographic data](https://www.aipla.org/list/innovate-articles/programmatic-patent-searches-using-google-s-bigquery-public-patent-data). So I'll read each family's US or English-language member, and record when none is available.

## What I changed from the draft

| Draft | Problem | My version |
|---|---|---|
| Don't rely on Google's table, as its data dates to 2018 | Not true of this table: it was last modified on 23 September 2026, with filings to August 2026 | Keep Google, and PATSTAT stays optional |
| Two independent annotators | There aren't two human experts here | Claude and me, with the limit stated |
| 300 families straight away | Expensive before the rules are tested | 90-family pilot first |
| 16 examples as a boundary test | None came from Arista, and few from Nokia or Cisco. Others came from Tigera and Quanta, which aren't in my comparison set | Sample by company |
| Started sampling before building a rival set | The sample couldn't reflect each company | Build the rival table first |
| Precision only, with recall as a note | Pools could miss a company's patents | Added a recall test and a company check |
| H04L 12 and G02B 6 as starting codes | Too broad | Not used alone |
| Three labels with no link to the question | Doesn't connect to the business | Mapped to Nokia's units, and added AI and cloud relevance |

I checked four of its 16 examples on Google Patents. The owners matched, and EP3410735A1's first claim and US20170063631A1's first claim support its labels. The other 12 and its claim-based reasoning aren't verified.
