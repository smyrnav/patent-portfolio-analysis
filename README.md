# Nokia–ICEYE Sovereign LEO Communications

**Ukraine's sovereign alternative to Starlink — technology, patent portfolio and strategic investment analysis**

*"Alternative to Starlink" is the headline framing; the partners describe the system as complementing, not replacing, existing networks — see the [pivot document](docs/01-research-design/pivot-sovereign-satcom.md).*

**Independent research project | [Financial Data Engineering / Business Data Analytics Trainee](https://www.linkedin.com/jobs/view/4483030441) application, Business Data Analytics track**[^1]

Not affiliated with Nokia.

## Why this repo exists

I saw Nokia's Financial Data Engineering / Business Data Analytics Trainee vacancy and opened this repository to teach myself the analytics the role calls for. Patent portfolio analysis was new territory for me, so this project is a deliberate, working-in-the-open learning exercise: pick a real question, source public data, build the pipeline, document every assumption, and keep the record honest about what holds up and what doesn't. The goal is a defensible work sample for that vacancy — and, along the way, a genuinely learned skill set.

The question sharpened as I worked — I pivoted and re-aimed the research questions more than once as the evidence demanded. Then, in October 2026, ICEYE and Nokia announced a sovereign LEO satellite communications partnership, and on 22 October signed a Letter of Intent with Ukraine's Ministry of Defence. The news reached me like this:

<p>
  <img src="docs/01-research-design/assets/pivot-trigger-1-headline-sq.jpg" alt="Nokia partners with Ukraine to build a Starlink alternative" width="32%">
  <img src="docs/01-research-design/assets/pivot-trigger-2-loi-sq.jpg" alt="Letter of Intent with the Ministry of Defense of Ukraine, announced 22 October 2026" width="32%">
  <img src="docs/01-research-design/assets/pivot-trigger-3-partnership-sq.jpg" alt="Nokia and ICEYE: secure, sovereign LEO satellite communications for defense, border security and disaster response" width="32%">
</p>

I'm Ukrainian, and this pivot is fairly personal: secure communications that answer to Kyiv are critical infrastructure for my country rather than simply an abstract market investment opportunity. October 2026 showed why — a foreign vendor throttled Ukraine's service for ten days without warning and demonstrated how vulnerable the dependence itself is. Finland, on the other hand, has been a reliable and dependable ally in these unprecedentedly dark times, helping Ukraine defend itself and hosting thousands of Ukrainians. So naturally, participating in this project — and, hopefully, in the Nokia–ICEYE effort itself — is how I would like to contribute and, hopefully, this project can teach me something new and provide interesting and relevant insights for the company. All of these fields are quite new to me, so termology, appropriate research methodology and relevant data sources and validation methods are all learned along the way. Research itself, however, is not influenced by my own partiality or interest in the subject: the data, methods and checks are what they are, and the findings are evidence-supported.
## Research question

**Which technological capabilities, patent assets and investment priorities — observable in publicly available data — are most important for developing a sovereign LEO satellite communications capability for Ukraine and European government customers?**

The project [pivoted to sovereign satcom](docs/01-research-design/pivot-sovereign-satcom.md) on 2 November 2026, after ICEYE and Nokia signed a Letter of Intent with the Ministry of Defence of Ukraine. The [five research questions](docs/01-research-design/research-questions.md) operationalise it through the build–buy–partner–license framing.

## Analytical focus

- Satellite communications and non-terrestrial networks (NTN)
- Secure and resilient connectivity
- Ground infrastructure and network integration
- Satellite terminals and communications technology
- Patent portfolios, technological dependencies and competitors
- Strategic investment priorities

The pipeline was built and tested on optical networking, IP routing and data-centre switching. Those categories are being replaced by satellite-communications code pools per the [pivot checklist](docs/01-research-design/pivot-sovereign-satcom.md#checklist-to-execute-the-pivot); the results below predate the pivot and show the method, not the answer to the new question. [Full scope](docs/01-research-design/scope.md).

## Research objective

To examine Nokia's technology position, competitor activity, commercial developments and patent portfolio characteristics, and identify where investment could be maintained, expanded, reallocated or investigated further.

## Methodology

The research combines patent-family analysis, claim-based technology classification, competitor benchmarking, public financial and commercial information, geographic protection analysis and ten-year patent maintenance cost modelling.

Classification rules, assumptions and data transformations are documented so that the work can be rerun and checked. [Research design](docs/01-research-design/research-design.md).

## Data limitations

The research relies only on publicly available information. It doesn't include Nokia's internal patent spending, portfolio valuations, confidential licensing arrangements or internal R&D investment decisions.

So calculated indicators and recommendations are independent external assessments based on observable evidence. They aren't definitive assessments of Nokia's internal portfolio strategy.

## Data sources

| Data | Source | Notes |
|---|---|---|
| Patent publications and technology codes | [Google Patents public dataset in BigQuery](https://console.cloud.google.com/marketplace/product/google_patents_public_datasets/google-patents-public-data), supplied by IFI CLAIMS; table last modified 23 September 2026 | Queried with the SQL in [`sql/`](sql/README.md); local snapshots fingerprinted in [`data/source_manifest.csv`](data/source_manifest.csv) |
| Classification code definitions | [USPTO CPC scheme](https://www.uspto.gov/web/patents/classification/cpc/html/cpc-H04B.html) | Basis of the satcom code pools, checked 8 November 2026 |
| Nokia financials | [Nokia 20-F annual reports, FY2006–FY2025](data/raw/annual_reports_manifest.csv), via SEC EDGAR | Official filings |
| US renewal fees | [USPTO fee schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule) | Official; fees change, check before reuse |
| Ownership and renewal records | [USPTO bulk data portal](https://data.uspto.gov/bulkdata/datasets/ptmnfee2) | Not yet downloaded — the known ownership gap |

## Research status

**There's no answer to the central question yet.** [Full tracker](docs/appendices/evidence-gaps.md).

| Workstream | Status | Where it stands |
|---|---|---|
| Research design and scope | Defined | [Five research questions](docs/01-research-design/research-questions.md) |
| Candidate portfolio universe | Preliminary | [Counts are not verified rights or owners](docs/02-methodology/candidate-portfolio-universe.md) |
| Technology classification | Under validation | [Code pools failed my 85% precision bar](docs/02-methodology/validation.md#precision-result) on preliminary first-pass labels. Human hand-labelling, human–software agreement and recall not done |
| Competitor selection | Defined | [Peer selection](docs/03-market-and-patent-analysis/market-context-and-peer-selection.md) |
| Competitive patent analysis | First estimates | [Low confidence](docs/03-market-and-patent-analysis/patent-landscape.md) |
| Commercial and patent alignment | Pending | [Inputs collected](docs/03-market-and-patent-analysis/commercial-alignment.md) |
| Ten-year maintenance cost model | Designed, not built | [Q9 design](docs/04-financial-analysis/ten-year-maintenance-cost-model.md). US fees and a [break-even](docs/04-financial-analysis/us-renewal-break-even.md) done |
| Investment recommendations | Pending | [Provisional findings only](docs/05-findings-and-recommendations/findings.md) |

## Main results so far

### Patent codes alone can't compare companies

Preliminary software-assisted claim checks compared each code pool with what the patent claims actually say, with company, pool and codes hidden. These first-pass labels haven't been human reviewed.

| Code pool | Claims match, of 100 sampled | 95% range | 85% bar |
|---|---:|---|---|
| Optical | 73 | 64–81% | Fail |
| IP routing | 39 | 30–49% | Fail |
| Data-centre switching (H04L 49) | 42 | 33–52% | Fail |

### Nokia-lineage patents show far more transfers than competitors' patents

42 of 179 sampled Nokia-lineage patents (23.5%) show another current assignee on Google Patents, such as WSOU or RPX, against 2 of 242 for the other four companies. Google Patents isn't a register, so [this needs checking against USPTO records](docs/02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far).

### The candidate universe isn't a verified portfolio

![From 72,207 families to a candidate universe](docs/img/candidate_universe.png)

19,873 families have grant evidence and were filed within 20 years, and 5,595 more have a recent application with no grant detected. Absence of a detected grant isn't proof of pending status. Verified active rights and verified current owners are both still at 0.

### First estimates: strongest in optical, thinnest in switching

| Estimated US families (95% range) | Optical | IP routing | Switching |
|---|---|---|---|
| **Nokia lineage** | 768 (641–840) | 233 (151–329) | 70 (46–97) |
| Ciena | 263 (169–342) | 90 (47–146) | 40 (24–57) |
| Cisco, with Acacia and Luxtera | 233 (155–294) | 792 (410–1,284) | 220 (120–337) |
| Arista | 9 (5–12) | 143 (74–198) | 33 (14–57) |
| Huawei | 746 (423–950) | 714 (300–1,226) | 175 (73–300) |

Low confidence: small samples, recall untested, and not yet adjusted for transfers. [The adjusted version](docs/03-market-and-patent-analysis/patent-landscape.md#the-same-estimate-keeping-only-patents-without-another-current-assignee) lowers Nokia's switching estimate to 26.

### No single company leads AI and cloud networking

![No single company leads AI and cloud networking](docs/img/ai_cloud_leaders.png)

Market share isn't patent strength. [Sources and peer selection](docs/03-market-and-patent-analysis/market-context-and-peer-selection.md).

## Guide to the repo

| Folder | Contents |
|---|---|
| [1. Research design](docs/01-research-design/research-design.md) | The protocol, [scope](docs/01-research-design/scope.md) and [research questions](docs/01-research-design/research-questions.md) |
| 2. Methodology | [Codebook](docs/02-methodology/classification-codebook.md), [validation](docs/02-methodology/validation.md), [candidate universe](docs/02-methodology/candidate-portfolio-universe.md), [data quality and lineage](docs/02-methodology/data-quality-and-lineage.md), [metrics](docs/02-methodology/metrics.md) |
| 3. Market and patent analysis | [Peer selection](docs/03-market-and-patent-analysis/market-context-and-peer-selection.md), [patent landscape](docs/03-market-and-patent-analysis/patent-landscape.md), [commercial alignment](docs/03-market-and-patent-analysis/commercial-alignment.md), [twenty years of reported figures](docs/03-market-and-patent-analysis/twenty-years.md) |
| 4. Financial analysis | [Ten-year cost model](docs/04-financial-analysis/ten-year-maintenance-cost-model.md), [assumptions and scenarios](docs/04-financial-analysis/assumptions-and-scenarios.md), [US break-even](docs/04-financial-analysis/us-renewal-break-even.md) |
| 5. Findings | [Findings so far](docs/05-findings-and-recommendations/findings.md) |
| Appendices | [Progress tracker](docs/appendices/evidence-gaps.md), [fact checks](docs/appendices/sources.md), [data map](docs/appendices/data-map.md), [working principles](docs/appendices/working-principles.md) |
| How I learned | [Learning log](docs/appendices/learning-log.md), [research log](docs/appendices/research-log.md), [question notebook](docs/appendices/questions.md), [knowledge check](docs/appendices/explain-it.md) |
| Code and data | [`sql/`](sql/README.md), [`src/`](src), [`tests/`](tests), [`data/`](docs/appendices/data-map.md#repository-data-folders), [`config/`](config/research_parameters.toml) |

## Run it yourself

```bash
python3 src/run_all.py
```

That reruns the cleaning, scoring, checks and tests, using only the standard library and Python 3.11 or later. To redraw the charts as well:

```bash
pip install -r requirements.txt
python3 src/run_all.py --charts
```

To get Nokia's annual reports, set your own contact, as the SEC requires one:

```bash
SEC_USER_AGENT="Your Name you@example.com" python3 src/download_annual_reports.py
```

The reports stay out of the repo because of their size, and [the manifest](data/raw/annual_reports_manifest.csv) records each file's source and fingerprint. BigQuery steps are listed in [`sql/README.md`](sql/README.md) and consolidated cell by cell in [`notebooks/patent_portfolio_queries.ipynb`](notebooks/patent_portfolio_queries.ipynb); they rebuild the sandbox tables, which expire after 60 days.

## How this was made

I chose the question, sources and method, and I am responsible for the methods, validation, calculations and conclusions. I used Claude for script drafting, browser-assisted query execution, document drafting and software-generated first-pass patent labels, and Kimi for a repository-structure review. Those labels haven't been human reviewed; the [validation page](docs/02-methodology/validation.md#who-labelled-what) records what remains to be checked.

[^1]: *What would you do with all the patent data in the world?* First probably go a little insane organising, deduplicating, cleaning and validating it — and only then produce findings solid enough to base a business strategy on; nevertheless, I'd try.
