# Nokia–ICEYE: Patent Portfolio Research for Sovereign Satellite Communications

**What does publicly available patent data reveal about the satellite-communications patent portfolios of Nokia, ICEYE and selected competitors, and how reliable are those comparisons?**

Independent research project, developed in connection with the [Financial Data Engineering / Business Data Analytics Trainee](https://www.linkedin.com/jobs/view/4483030441) application at Nokia. Not affiliated with or endorsed by Nokia or ICEYE.

## Why this repo exists

Patent portfolio analysis was new to me, so I built this as a practical work sample: a real question, public data, a working pipeline, and honest documentation of what holds up and what doesn't. When Nokia and ICEYE announced their sovereign LEO satellite communications partnership in October 2026 (with a Letter of Intent to Ukraine's Ministry of Defence on 22 October), the project moved to that subject.

## What I investigate

Two workstreams, one subject. Neither measures operational capability.

**1. Patent research** (the core). Collect patent records from Google Patents' public BigQuery dataset, identify company applicants and their historical names, group publications into patent families, find candidate satellite-communications patents via CPC codes, and check those candidates by reading patent claims. Company portfolios are compared only when the classification proves reliable enough.

**2. Procurement research** (demand side, separate). What do Ukrainian public procurement records show about government purchases and planned purchases of satellite-related equipment and services? Data: the Prozorro portal API. Details: [procurement-demand.md](docs/01-research-design/procurement-demand.md).

## What I have found so far

**Established (within stated scope):**

- Under the current candidate pools and name matching, no Ukrainian corporate assignees appear: 16 individual inventors with one family each, and 16 satcom-pool families ever filed at the Ukrainian office by 10 foreign owners ([queries 25–28](sql/README.md)). This says nothing about Ukrainian engineering capability.
- Overall portfolio sizes in the dataset (all technologies, name-matched): Airbus 19,488 families, Thales 9,873, Viasat 822, ICEYE 53 ([query 24](sql/README.md)). These are **not** satellite-communications counts.
- A name search finds 110 SpaceX-associated families ([query 30](sql/30_spacex_name_counts.sql)). Starlink's position cannot be measured through patent counts, so no patent-based comparison with Starlink is made.

**Preliminary:**

- ICEYE's 53 families sit mostly in radar (G01S, 35) and spacecraft operations (B64G, 14), with 7 in transmission (H04B); 6 fall in the candidate satcom pools. Classification-level results, not verified capabilities.

**Blocked — and it determines what the project can claim:**

- The technology sorting failed its own diagnostic on 13 November: 70.8% agreement between CPC-based sorting and software first-pass labels on a blind 144-patent sample, against this project's 85% acceptance rule ([full record](docs/02-methodology/satcom-validation-plan.md#stage-3-result-13-november-2026-the-re-test-failed-the-bar)). Human review is not done, so this is not a validated accuracy figure. Consequence: no company comparisons are published. The next task is redesigning the classification rules, then human validation.

## Current state

| Part | State |
|---|---|
| Patent data extraction and cleaning | Implemented |
| Patent family grouping | Implemented |
| Candidate technology classification | Preliminary — failed its diagnostic, redesign next |
| Reliable company comparisons | Blocked on classification validation |
| Starlink procurement extraction | Completed — 1,867 tenders, 4,050 plans |
| Multi-category procurement run | In progress |
| Business conclusions | Preliminary |

## Where to start

| I want to understand... | Read |
|---|---|
| What the project investigates | [Research design](docs/01-research-design/research-design.md) |
| What was found | [Findings](docs/05-findings-and-recommendations/findings.md) |
| How patent classification works | [Classification codebook](docs/02-methodology/classification-codebook.md) |
| Whether the classifications can be trusted | [Validation plan](docs/02-methodology/satcom-validation-plan.md) |
| What is unfinished | [Evidence tracker](docs/appendices/evidence-gaps.md) |
| What the technical terms mean | [Glossary](docs/glossary.md) |
| How the SQL queries work | [SQL README](sql/README.md) |

## Running the project

Three separate activities:

1. **Local checks** — process saved files only, download nothing: `python3 src/run_all.py` (stdlib, Python 3.11+; steps needing local claim pages skip cleanly on a fresh clone).
2. **BigQuery patent extraction** — downloads new data, needs a Google Cloud account: queries and runner in [`sql/README.md`](sql/README.md).
3. **Prozorro extraction** — downloads new data: `python3 src/prozorro_pipeline.py` (config: [`config/prozorro_categories.yaml`](config/prozorro_categories.yaml)).

## How this was made

I chose the question, sources and method, and I am responsible for the methods, validation, calculations and conclusions. I used Claude for script drafting, query execution, document drafting and first-pass patent labels, and Kimi / Kimi Code for repository reviews and restructuring. The [validation page](docs/02-methodology/validation.md#who-labelled-what) records what a human still has to check.
