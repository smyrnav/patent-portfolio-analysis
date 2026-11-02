# Pivot: sovereign satellite communications

**Date:** 2 November 2026
**Status:** Decided. Canonical rewrite of the research question across the repository is the next step (see checklist below).

## Trigger

On 22 October 2026, ICEYE and Nokia signed a Letter of Intent with the Ministry of Defence of Ukraine to explore cooperation in space — sovereign, secure LEO satellite communications for defence, border security and disaster response ([Nokia press release via Yahoo Finance](https://uk.finance.yahoo.com/news/iceye-nokia-partner-ministry-defence-175200661.html), [Militarnyi](https://militarnyi.com/en/news/ukraine-iceye-and-nokia-join-forces-to-develop-indigenous-satellite-communications-system/), [The Defense Post](https://thedefensepost.com/2026/10/27/ukraine-sovereign-satcom-system/amp/)). This followed the ICEYE–Nokia strategic partnership announced on 6 October 2026 to develop sovereign satellite communications for government and defence customers, targeting a LEO constellation by 2028 ([Israel Defense](https://www.israeldefense.co.il/en/node/71424)).

This is a verified public fact. What a Letter of Intent will become — contract, programme, cancellation — is unknown and must not be treated as revenue.

## Why pivot

The original question asked how Nokia's patent portfolio supports its AI and cloud infrastructure strategy. The ICEYE partnership is the strongest public signal yet of where Nokia is actually placing a new bet: sovereign satellite communications and defence connectivity. Analysing that bet is more current, more distinctive as a work sample, and still squarely patent portfolio analytics — the skill set the vacancy calls for. The question changes; the craft doesn't.

## New central question (candidate)

> How should Nokia develop its patent portfolio to support a sovereign satellite communications and defence connectivity strategy?

This wording is provisional. The canonical question lives in `config/research_parameters.toml` and is enforced by `tests/test_repository.py`; switching it means updating every document in one pass so the consistency test stays green.

## What the analysis will be used for

1. **The application work sample.** Same vacancy, same standard: a defensible, reproducible, outside-in analysis. The pivot itself is evidence — recognising a material strategic event and re-aiming the research within days.
2. **The actual analysis.** Map Nokia's publicly observable patent position in satellite communications (payloads, inter-satellite links, ground segment, secure waveforms, network integration), benchmark it against the actors that matter in sovereign satcom, and ask what Nokia has, what ICEYE adds, and where the gaps are.
3. **A living portfolio.** The repo stays honest: this document records the pivot, the old question stays in the change history, nothing is silently rewritten.

## What survives the pivot

- The entire pipeline: BigQuery dataset, entity resolution, family building, grant-evidence logic, validation method, cost model framework.
- The five-question structure (position → comparison → business fit → cost → priorities) — the questions get re-aimed, not replaced.
- The honesty machinery: evidence labels, assumptions register, precision bar, tests.
- The Alcatel/Lucent lineage work — Nokia Bell Labs and legacy satellite-adjacent research still flow through the same lineage.

## What changes

| Element | Was | Becomes |
|---|---|---|
| Technology categories | OPT / IPR / DCS | New satcom code pools (e.g. H04B 7/185 satellite comms, H04K/H04L security, plus ground-segment and optical inter-satellite link codes — to be defined from CPC, not guessed) |
| Peers | Ciena, Cisco, Arista, Huawei | Rethought per category: ICEYE (partner, not peer), Eutelsat/OneWeb, Viasat, Thales Alenia Space, Airbus Defence and Space; SpaceX noted as the dominant actor with limited patent transparency |
| H1–H4 | Optical/routing/switching hypotheses | Retired to the log; new hypotheses drafted after the code pools exist |
| Classification validation | 300-family sample in OPT/IPR/DCS | New sample in the new categories — nothing carries over as validated |
| Infinera analysis | H1 driver | Becomes background; still answers "what Nokia bought in optical transport," which feeds ground-segment backhaul |

## What this pivot must not do

- Treat the Letter of Intent as a contract, programme or revenue.
- Assume Nokia's satcom patent position is strong (or weak) before measuring it.
- Reuse the OPT/IPR/DCS precision results as if they validate satcom classification.
- Drop the old work as wasted: the pipeline, the validation method and the financial model are exactly what the new question needs.

## Checklist to execute the pivot

1. Define satcom CPC/IPC code pools from the classification schedules, with sources.
2. Rewrite the central question in `config/research_parameters.toml`, README and research design in one pass; keep the consistency test green.
3. Re-aim RQ1–RQ5 and retire H1–H4 to this log.
4. Run pool counts for Nokia, ICEYE and the new peer set in BigQuery.
5. New validation sample before any comparative claim.
6. Update README status table and the executive brief.
