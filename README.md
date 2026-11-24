# Nokia–ICEYE Sovereign LEO Communications

**Ukraine's sovereign alternative to Starlink — technology, patent portfolio and strategic investment analysis**

*"Alternative to Starlink" is the headline framing; the partners describe the system as complementing, not replacing, existing networks — see the [pivot document](docs/01-research-design/pivot-sovereign-satcom.md).*

*The vacancy asks: "What would you do with all the patent data in the world?" First probably go a little insane organising, deduplicating, cleaning and validating it — and only then produce findings solid enough to base a business strategy on; nevertheless, I'd try.*

**Independent research project | [Financial Data Engineering / Business Data Analytics Trainee](https://www.linkedin.com/jobs/view/4483030441) application, Business Data Analytics track**

Not affiliated with Nokia.

## Why this repo exists

I saw Nokia's Financial Data Engineering / Business Data Analytics Trainee vacancy and opened this repository to teach myself the analytics the role calls for. Patent portfolio analysis was new territory for me, so this project is a deliberate, working-in-the-open learning exercise: pick a real question, source public data, build the pipeline, document every assumption, and keep the record honest about what holds up and what doesn't. The goal is a defensible work sample for that vacancy — and, along the way, a genuinely learned skill set.

The question sharpened as I worked — I pivoted and re-aimed the research questions more than once as the evidence demanded. Then, in October 2026, ICEYE and Nokia announced a sovereign LEO satellite communications partnership, and on 22 October signed a Letter of Intent with Ukraine's Ministry of Defence. The news reached me like this:

<p>
  <img src="docs/01-research-design/assets/pivot-trigger-1-headline-sq.jpg" alt="Nokia partners with Ukraine to build a Starlink alternative" width="32%">
  <img src="docs/01-research-design/assets/pivot-trigger-2-loi-sq.jpg" alt="Letter of Intent with the Ministry of Defense of Ukraine, announced 22 October 2026" width="32%">
  <img src="docs/01-research-design/assets/pivot-trigger-3-partnership-sq.jpg" alt="Nokia and ICEYE: secure, sovereign LEO satellite communications for defense, border security and disaster response" width="32%">
</p>

This pivot is of both professional and analytical interest: secure communications that answer to the government using them are critical infrastructure, not an abstract market trend. October 2026 showed why — a foreign vendor throttled Ukraine's service for ten days without warning and demonstrated how vulnerable the dependence itself is. So participating in this project — and, hopefully, in the Nokia–ICEYE effort itself — is a chance to learn something new and provide relevant insights for the company. All of these fields are quite new to me, so terminology, appropriate research methodology and relevant data sources and validation methods are all learned along the way. The research itself is not influenced by personal interest in the subject: the data, methods and checks are what they are, and the findings are evidence-supported.

## What the project is about now

A sovereign satellite communications system needs five kinds of technology: the satellites themselves, ground stations, user terminals, the network software that ties space and ground together, and security (encryption, anti-jamming). Building one creates three business problems:

1. Do Nokia and ICEYE already hold the technology they need, or must they buy or license it from someone?
2. Could competitors' patents get in the way?
3. What should their engineers and IP lawyers check before serious money is committed?

This project researches the part of those problems that is visible in public patent data: who filed which inventions, in which technologies, where and when. That is one input — no more. Patent data cannot tell us whether the technology works, what development costs, what Nokia and ICEYE agreed between themselves (their split of work and IP is not public), or whether a specific patent would actually block the system — that last one is a legal judgment, case by case. Where the data can't answer, this repo says so instead of guessing.

The formal research question (kept word-for-word identical across the repo by an automated test):

> **What can Nokia and ICEYE realistically reuse from their existing technology assets to deliver a sovereign satellite communications system, and what must they develop, acquire or obtain from other partners?**

Re-aimed 24 November 2026. The earlier wording asked which capabilities, patent assets and investment priorities mattered most — too broad, and it invited investment conclusions public data can't support. The [three research questions](docs/01-research-design/research-questions.md) break the new one into answerable parts. New to patent data? The [glossary](docs/glossary.md) explains every term used here in plain language.

## What I actually do here

1. Pull patent records from Google's public patent dataset (BigQuery).
2. Clean up company names, so "Nokia", "Alcatel-Lucent" and "Infinera" count as one lineage.
3. Count each invention once (a patent family), even if it was filed in twenty countries.
4. Sort patents into the five technology buckets above — and **check the sorting by actually reading the patents**. Current status: the sorting failed its own accuracy test on 13 November (70.8% correct against an 85% requirement). Until it passes, no company comparisons are published. Fixing the sorting rules is the next real task.
5. Only after the buckets pass: compare Nokia, ICEYE and competitors, and write up what that means for the three business problems.

Separately, the repository now also tracks the demand side: what Ukrainian and European government buyers actually purchase in satellite communications, through public procurement records ([Prozorro pipeline](docs/01-research-design/procurement-demand.md)). Patents show who owns technology; procurement shows who buys it, at what price, and where the current supply fails.

Everything is scripted and can be rerun: [`sql/`](sql/README.md) for the queries, [`src/`](src) for the pipeline, [`tests/`](tests) for the consistency checks.

## What we know so far

Four findings stand, each with its query and data on file:

- **Ukraine has no domestic satellite-communications patent base.** Sixteen individual inventors with one family each; no companies. Only 16 satcom patent families were ever filed at the Ukrainian patent office, by 10 foreign owners. So the system's technology will be foreign-patented, and the terms of access (license, partnership, purchase) become the real sovereignty question. This says nothing about Ukrainian engineering ability — patents don't measure that, and classified defence work never patents. ([queries 25–28](sql/README.md))
- **ICEYE's patent record is radar and satellite platforms, not communications.** 53 patent families: 35 radar imaging, 14 spacecraft operations, only 7 in transmission. My working guess, labelled as a guess: the communications technology in the partnership comes from Nokia. The actual split is not public, and few patents does not mean little capability. ([queries 24, 35, 36](sql/README.md))
- **The incumbents hold deep patent positions.** Airbus ~19,500 families, Thales ~9,900, Viasat ~800 in our cleaned data. Anyone building in this space builds next to those positions — that's where dependency risk would come from.
- **Patent data can't see the market leader.** SpaceX holds only 110 families — it keeps technology as trade secrets. So no patent-based comparison with Starlink is possible, and I say so wherever comparisons appear. ([query 30](sql/30_spacex_name_counts.sql))

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

Reruns the cleaning, scoring, checks and tests with only the standard library (Python 3.11+). On a fresh clone, the two steps that need my local patent-claim pages (gitignored, since they mirror claim text) skip themselves cleanly and keep the committed results. Add `--charts` (needs `pip install -r requirements.txt`) to redraw the charts. BigQuery steps are listed in [`sql/README.md`](sql/README.md).

## How this was made

I chose the question, sources and method, and I am responsible for the methods, validation, calculations and conclusions. I used Claude for script drafting, query execution, document drafting and first-pass patent labels, and Kimi / Kimi Code for repository-structure reviews and the 24 November restructure. The [validation page](docs/02-methodology/validation.md#who-labelled-what) records exactly what a human still has to check.
