# Metrics

Each measure used in the project, and what it's measured against.

## Patent units

| Term | Meaning | Example |
|---|---|---|
| **Publication** | One published document | 289,998 in the working table |
| **Application** | One filing at one office, which may publish more than once | 212,660 |
| **Simple family** | One invention across offices, by Google's `family_id` | 72,207 |
| **National right** | One granted patent in one jurisdiction. Fees are paid at this level | Not counted yet |

## Classification measures

| Measure | Calculation | Reported in |
|---|---|---|
| **Pool precision** | Patents whose claims earned the class ÷ patents sampled from that code pool | [Validation](validation.md#precision-result) |
| **95% range** | Wilson interval on that share | [Validation](validation.md#precision-result) |
| **Estimated families** | US families in the pool × the share of that company's sample whose claims earned the class. The range only reflects sampling of that share | [Patent landscape](../03-market-and-patent-analysis/patent-landscape.md) |
| **Human–software agreement** | Cohen's kappa between the software-generated first pass and independent human hand-labels, targeting 100 sampled families per primary category (300 total); this compares me against the software, not against a second person | Not measured yet |
| **Recall** | Share of relevant families that the pools find | Not measured yet |

## Measured so far

| Measure | Mean | Median | Middle 80% | Records |
|---|---:|---:|---:|---:|
| US years to grant | 4.27 | 4.05 | 2.16–6.66 | 10,855 patents |
| European years to grant | 6.17 | 5.79 | 2.79–9.92 | 6,417 patents |
| Chinese years to grant | 4.89 | 4.88 | 3.67–6.08 | 2,278 patents |
| Applications per family with grant evidence | 3.68 | 3 | 1–6 | 19,873 families |
| Offices per family with grant evidence, including international filings | 3.43 | 3 | 1–6 | 19,873 families |

[Source](../../data/processed/patent_measures.csv). Time to grant covers filings from November 2006 to 2015, so recent cases don't skew it short. Filings per family are low, because they rely on applicant names and miss some records, such as many Japanese ones. Filing somewhere doesn't mean a patent is being maintained there.

## Indicators, not value

| Indicator | What it can suggest | What it can't show |
|---|---|---|
| Family count | Scale of activity in an area | Quality or commercial value |
| Citations | Influence, once adjusted for age. Missing on 49% of publications | Value |
| Offices filed | Where protection was sought | Where it's still paid for |
| Renewal behaviour | What owners chose to keep | Why they kept it |

## Ratios I don't use

| Ratio | Why |
|---|---|
| Renewal fees as a share of licensing sales | Sales depend on far more than fees, and it doesn't establish financial efficiency |
| Licensing sales per family | Income is usually concentrated in a few programmes, and the family count includes patents held by others |
| R&D rankings across companies | [The figures have different boundaries](../03-market-and-patent-analysis/market-context-and-peer-selection.md#commercial-context) |
