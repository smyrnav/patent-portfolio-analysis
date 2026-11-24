# What governments actually buy — procurement evidence

**Status: initial dataset.** 1,867 Starlink tender records and 4,050 procurement plans extracted 24 November 2026 (`data/raw/prozorro_starlink_*.csv/.json`). The multi-category pipeline (19 queries, 5 categories) exists in code and config; its full run is in progress, so cross-category outputs are not yet available. This is a demand-side dataset under construction, not a completed market analysis.

Patent data shows who *owns* technology. It says nothing about who *buys* it. Procurement records are the missing demand side: they show real buyer behaviour — signed contracts, real prices, real technical requirements — not analyst forecasts.

## The question this answers

**Which government needs for satellite communications remain active, how are they being met today, and is there an opening for a new supplier to offer a better alternative?**

We are not building a catalogue of Starlink purchases for its own sake. The data answers the question in three parts:

| Part | What answers it | Where in the data |
|---|---|---|
| **Which needs are still active?** | What is being bought right now, in what volumes, and what buyers ask for in tender texts | Tenders by year, titles and item descriptions; the count of currently active procurements |
| **How are they met today?** | Who wins contracts, with what suppliers, and how concentrated the supply is | Contracts: suppliers with EDRPOU codes, statuses, dates |
| **Is there an opening for a new supplier?** | Signals that buyers accept alternatives, and where buying attempts fail | Tenders titled "Starlink **або еквівалент**" (Ukrainian procurement law forces this wording — buyers must accept equivalents), plus unsuccessful and cancelled tenders |

That third part is where this work meets the central research question: an alternative supplier (for example the Nokia–ICEYE sovereign offering) wins not by being mentioned in patents, but by fitting the requirements buyers already write down. Procurement data is the only public source that shows those requirements, the prices paid and the failures of the current supply.

This feeds [RQ1](research-questions.md): the capability map should be built from what buyers require, not from what I imagine the system needs. It also gives [RQ3](research-questions.md) context on who the buyers are and what a contract looks like.

## Sources

| Source | Covers | Access |
|---|---|---|
| [Prozorro](https://prozorro.gov.ua) | Ukrainian public procurement — Starlink terminals, satellite equipment, internet services already appear there | Free, public |
| [TED (Tenders Electronic Daily)](https://ted.europa.eu) | EU government procurement — defence communications, satellite services, secure connectivity | Free, public |

## What to extract from each tender

- **Who buys:** ministry, military unit, emergency service.
- **What they buy:** terminals, equipment, network access, or a full service.
- **How much and to what spec:** quantities and the technical requirements in the tender text.
- **Money:** expected vs. final price.
- **Who wins:** supplier, contract length, service terms.

## Honest limits

- **Expected value is not expenditure.** Tender rows carry the expected procurement value; what was actually paid is known only from signed contract records, and awarded amounts can differ.
- **A failed tender is not automatically unmet demand.** Unsuccessful or cancelled tenders can mean bad specs, unrealistic prices, timing, or paperwork — the reasons sit in each tender's documents, not in its status.
- Prozorro and TED today mostly show purchases of *existing foreign systems* (Starlink above all). That is evidence about demand and requirements — not about the Nokia–ICEYE offer, which is a Letter of Intent, not a tender.
- Classified defence procurement is invisible, and in wartime Ukraine that is a large blind spot.
- The Starlink extraction is one search query, not the whole satellite-communications market; other operators and generic satellite equipment come from the multi-category run.
- No aggregate claims ("the market is worth X") until tenders are extracted one by one and the numbers can be shown per contract.

## How the search is extracted

The portal search page is a JavaScript app; its underlying endpoint is public and needs no login:

```
POST https://prozorro.gov.ua/api/search/tenders?text=Starlink&page=1
```

Two limits shape the extraction: results are capped at **1,000 per search** (page 51 is rejected, per_page fixed at 20), and each row carries only summary fields — buyer name, title, tenderID, expected value with currency, status, period dates. Contract prices and technical requirements live inside each tender's own page, a second extraction step.

The [`prozorro_extractor`](../../src/prozorro_extractor.py) module works around the cap by splitting the notice-date range into shards small enough to stay under 1,000 hits, paging each shard and deduplicating by tenderID. Run it as a script (`python3 src/prozorro_extractor.py --text Starlink`) or import `extract(text, start, end)` from it; the sharding logic is covered by offline tests. Output: `data/raw/prozorro_starlink_tenders.csv` (flat table with links) and `data/raw/prozorro_starlink_tenders.json` (raw items).

## First step (cheap, before building anything)

Manually read 10–20 Starlink/satellite tenders in Prozorro and check whether the fields above are actually filled in. If they are, this becomes a proper workstream with a saved extraction sheet. If they aren't, the idea is recorded here and dropped — one afternoon settles it.
