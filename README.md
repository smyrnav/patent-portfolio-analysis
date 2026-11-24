# Nokia–ICEYE Sovereign LEO Communications

**Exploring the technology, patent landscape, and strategic considerations behind a sovereign satellite communications capability for Ukraine.**

*The project was widely described as Ukraine's "Starlink alternative" after a foreign provider restricted Ukraine's satellite service without warning for ten days. The disruption highlighted the risks of relying on an external network. Nokia and ICEYE describe their proposed system as a complement to existing military, commercial, and government networks, not a replacement. [Background and sources](docs/01-research-design/pivot-sovereign-satcom.md).*


**Independent research project | Developed in connection with the [Financial Data Engineering / Business Data Analytics Trainee](https://www.linkedin.com/jobs/view/4483030441) application, Business Data Analytics track.**

*Not affiliated with or endorsed by Nokia or ICEYE.*

## Why this repo exists

I came across Nokia's Financial Data Engineering / Business Data Analytics Trainee vacancy and started this repository as a way to develop the analytical skills the role calls for.

Patent portfolio analysis was new to me, so I approached this as a practical learning project: starting with a real question, working with public data, and building the pipeline needed to analyse it. I document the methodology, assumptions and limitations along the way, aiming to produce a useful work sample while learning the process behind the results.

The research questions changed as I worked through the data and figured out what was worth investigating. Since I am not a subject-matter expert on satcom, I learned about the terminology and industry as I worked with each dataset.

Then, in October 2026, Nokia and ICEYE announced a partnership on sovereign LEO satellite communications. On 22 October, they also signed a Letter of Intent with Ukraine's Ministry of Defence.

<p>
  <img src="docs/01-research-design/assets/pivot-trigger-1-headline-sq.jpg" alt="Nokia partners with Ukraine to build a Starlink alternative" width="32%">
  <img src="docs/01-research-design/assets/pivot-trigger-2-loi-sq.jpg" alt="Letter of Intent with the Ministry of Defense of Ukraine, announced 22 October 2026" width="32%">
  <img src="docs/01-research-design/assets/pivot-trigger-3-partnership-sq.jpg" alt="Nokia and ICEYE: secure, sovereign LEO satellite communications for defense, border security and disaster response" width="32%">
</p>

I came across the announcement while working on the project. The timing was unexpected, and it gave the research a new dimension.

## What the project is about now

A sovereign satellite communications system needs five kinds of technology: the satellites themselves, ground stations, user terminals, the network software that ties space and ground together, and security (encryption, anti-jamming). Building one creates three business problems:

1. Do Nokia and ICEYE already hold the technology they need, or must they buy or license it from someone?
2. Could competitors' patents get in the way?
3. What should their engineers and IP lawyers check before serious money is committed?

This project examines the patent portfolios of Nokia, ICEYE and selected competitors to understand their positions in satellite communications technologies. The repository contains the SQL and Python tools used to collect, clean, group and analyse patent data, map technology areas, validate classifications against patent claims, and bring together the market and financial context needed to interpret the findings.

The formal research question (kept word-for-word identical across the repo by an automated test):

> **What can Nokia and ICEYE realistically reuse from their existing technology assets to deliver a sovereign satellite communications system, and what must they develop, acquire or obtain from other partners?**

Updated 24 November 2026. The project now focuses on three research questions that can be investigated using public data. See the [research questions](docs/01-research-design/research-questions.md) and [plain-language glossary](docs/glossary.md).

## What I actually do here

1. Pull patent records from Google's public patent dataset (BigQuery).
2. Clean company names, so "Nokia", "Alcatel-Lucent" and "Infinera" count as one lineage.
3. Count each invention once (a patent family), not once per country.
4. Sort patents into the five technology buckets — and verify the sorting by reading the patents. On 13 November it failed its own accuracy test (70.8% against the 85% requirement), so company comparisons are on hold until the rules are fixed. That fix is the next real task.
5. Only then: compare Nokia, ICEYE and competitors, and write up what it means for the three business problems.

The repository also tracks the demand side through public procurement ([Prozorro pipeline](docs/01-research-design/procurement-demand.md)): who buys what, at what price — and which tenders fail. Unsuccessful and cancelled tenders are unmet demand: buyers the current market could not supply.

```mermaid
flowchart TD
    A["config/prozorro_categories.yaml<br/>5 categories · 19 search queries"] --> B["Prozorro portal search API<br/>POST /api/search/tenders · /contracts"]
    B --> C["Date sharding + pagination<br/>date ranges split until every shard is under the 1,000-result cap"]
    C --> D["Global deduplication<br/>one record per tenderID / contractID,<br/>every matching query and category kept"]
    D --> E["Raw JSONL + checkpoints<br/>evidence for every row, resume after interruption"]
    E --> F["Stage 1 · Bulk base<br/>tenders.csv · contracts.csv · matches.csv · tender cards"]
    F --> G["Stage 2 · Filter<br/>signed contracts only, ranked by value, top 50"]
    G --> H["Stage 3 · Selective details<br/>contract_details.csv · tech_requirements.csv"]
    F --> I["quality.csv<br/>shards, pages, duplicates, INCOMPLETE flags"]
    F --> J["prozorro_satellite_research.xlsx"]
    style A fill:#124191,color:#ffffff
    style B fill:#124191,color:#ffffff
    style C fill:#124191,color:#ffffff
    style D fill:#124191,color:#ffffff
    style E fill:#124191,color:#ffffff
    style F fill:#5B7DB8,color:#ffffff
    style G fill:#E6EAF0,color:#1A1A1A
    style H fill:#E6EAF0,color:#1A1A1A
    style I fill:#5B7DB8,color:#ffffff
    style J fill:#5B7DB8,color:#ffffff
```

Everything is scripted and can be rerun: [`sql/`](sql/README.md) for the queries, [`src/`](src) for the pipeline, [`tests/`](tests) for the consistency checks.

## What we know so far

Four findings stand, each with its query and data on file:

- **Ukraine has no domestic satellite-communications patent base.** 16 individual inventors with one family each; no companies. 16 satcom families ever filed at the Ukrainian office, all foreign-owned. The system's technology will be foreign-patented — so the terms of access are the real sovereignty question. Patents don't measure engineering ability; this says nothing about Ukraine's engineers. ([queries 25–28](sql/README.md))
- **ICEYE's patent record is radar and satellite platforms, not communications.** 53 families: 35 radar imaging, 14 spacecraft operations, 7 transmission. Working guess, labelled as such: the partnership's comms IP comes from Nokia — the actual split is undisclosed, and few patents does not mean little capability. ([queries 24, 35, 36](sql/README.md))
- **The incumbents hold deep patent positions.** Airbus ~19,500 families, Thales ~9,900, Viasat ~800. That is where dependency risk would come from.
- **Patent data can't see the market leader.** SpaceX holds 110 families — a trade-secret strategy, not a technology gap. No patent-based comparison with Starlink is possible. ([query 30](sql/30_spacex_name_counts.sql))

## Honest status

| Part | State |
|---|---|
| Data pipeline (extraction, cleaning, deduplication) | Works, reproducible |
| Ukraine domestic-base analysis | Done (above) |
| Prozorro procurement pipeline | 1,867 Starlink tenders and 4,050 plans extracted; full multi-category run in progress |
| Technology sorting into five buckets | **Failed its own accuracy test** — being redesigned |
| Company comparisons | On hold until the sorting passes |
| Old optical-networking analysis | [Archived](archive/pre-pivot/) — different question, kept as proof of method |
| Ten-year patent cost model | [Parked](archive/parked-financial-analysis/) — answered a question nobody is asking right now |

Full detail: [research design](docs/01-research-design/research-design.md) · [research questions](docs/01-research-design/research-questions.md) · [findings with evidence](docs/05-findings-and-recommendations/findings.md) · [progress tracker](docs/appendices/evidence-gaps.md) · [glossary in plain language](docs/glossary.md)

## Run it yourself

```bash
python3 src/run_all.py
```

Reruns the cleaning, scoring, checks and tests (stdlib only, Python 3.11+). Steps that need local claim-review pages (gitignored) skip cleanly on a fresh clone. Add `--charts` to redraw charts (needs `pip install -r requirements.txt`). BigQuery steps: [`sql/README.md`](sql/README.md).

## How this was made

I chose the question, sources and method, and I am responsible for the methods, validation, calculations and conclusions. I used Claude for script drafting, query execution, document drafting and first-pass patent labels, and Kimi / Kimi Code for repository-structure reviews and the 24 November restructure. The [validation page](docs/02-methodology/validation.md#who-labelled-what) records exactly what a human still has to check.
