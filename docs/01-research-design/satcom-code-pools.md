# Satellite communications code pools

**Status: accepted 11 November 2026, as amended by the pilot decisions R1–R5** ([record](../02-methodology/satcom-validation-plan.md#pilot-results-and-diagnosis-10-november-2026)). The acceptance does not make the pools *validated*: no comparative claim may use them until a new validation sample passes, per the pivot rule that nothing carries over from the pre-pivot categories.

## What the system must do

The partner announcements describe the system as three layers the customer nation owns outright — satellites, ground segment and user terminals ([sources](../appendices/sources.md#sovereign-satcom-context-post-pivot)). Read together with the October 2026 throttling incident and the contested-orbit threat record, that gives six capabilities a sovereign LEO satcom system needs:

| # | Capability | Why the central question depends on it |
|---|---|---|
| 1 | **Space segment payload** — the communications equipment on the satellite: bent-pipe or regenerative payload, beamforming | Without payload technology, "sovereign" means buying the hardest part from someone else |
| 2 | **Inter-satellite links** — moving traffic between satellites in orbit, radio or optical | Lets the constellation work without ground stations in territory the customer doesn't control |
| 3 | **Ground segment** — gateways, network operations | The layer the customer must own outright for the sovereignty claim to hold |
| 4 | **User terminals** — ruggedised terminals for field use | The layer the user actually touches; Nokia's tactical-radio products live here |
| 5 | **Network integration** — interworking with terrestrial networks (3GPP non-terrestrial networks), handover between satellites and to ground networks | The system is described as complementing, not replacing, existing networks; integration is where that promise is kept |
| 6 | **Security and resilience** — encryption, protection against jamming, geofencing, preventing unauthorised access | The pivot's trigger was a demonstrated dependence vulnerability; resilience is the point of the exercise, not a feature |

These describe what the system needs. They are not yet patent categories — that translation is next, and it has to survive validation before it means anything.

## From capabilities to candidate codes

The rule carried over from the [codebook](../02-methodology/classification-codebook.md): **CPC codes are only a search tool.** The patent office's category labels tell us which patents are *probably* about a topic. What a patent is really about is decided by the numbered sentences at the back of the patent document, where the inventor states in their own words exactly what they invented and own — the patent world calls these the "claims" (see the [glossary](../glossary.md)). So the codes pick the pile, and a human reading those numbered sentences makes the call. Pools are deliberately narrow; they get broadened only if the recall test shows misses. Every code below was read from the [CPC scheme](#sources), not guessed.

| Pool | Covers capability | CPC codes | What the code covers (scheme wording, shortened) |
|---|---|---|---|
| **SAT** | 1 (payload) | H04B 7/1851; H04B 7/18515; H04B 7/195 | Systems using a satellite or space-based relay; transmission equipment in satellites; non-synchronous stations (the LEO/MEO case — sits under the relay branch H04B 7/15) |
| **ISL** | 2 (links between satellites) | H04B 7/18521; H04B 10/118 | Systems of inter-linked satellites; free-space optical transmission specially adapted for satellite communication. **Reporting flag inside SAT, not a standalone bucket** (decision R5). Free-space optical patents count as ISL even when their numbered sentences never say "satellite" — that is what the code exists to cover (decision R4) |
| **GRD** | 3 and 4 (ground and terminals) | H04B 7/18517; H04B 7/18528 | Transmission equipment in earth stations; fixed satellite service / VSAT systems |
| **NET** | 5 (network integration) | H04W 84/06; H04B 7/18584; H04B 7/18541 | Airborne or satellite networks; data packet routing in satellite broadband systems; handover of resources in satellite systems |
| **SEC** | 6 (security and resilience) | Co-occurrence: any satellite pool prefix above **and** H04K 1/ or H04K 3/ | Countermeasures against jamming; secret communication. **Rebuilt after the pilot**: security codes alone caught terrestrial security patents 86% of the time, so a patent enters SEC only when a satellite code and a security code appear together (decision R1). The satellite-specific access codes H04B 7/18565 and 7/18593 stay as watch items: too rare to sample |

**The primary comparative measure is the combined satcom capability pool** — a family in any of the five pools — because the pilot showed the main defect is patents landing in the wrong sub-bucket, not non-satellite junk (decision R2). Single-pool comparisons are reported as tentative until the re-test.

## Deliberately left out, with reasons

| Code area | Why it's out |
|---|---|
| H04L 9 and H04L 63 (cryptography, network security generally) | Too broad to use alone — the same lesson as H04L 47 in the pre-pivot pilot. Satellite security candidates come through the SEC pool's satellite-specific codes |
| B64G (spacecraft design and control) | Platforms, not communications. The question is about the communications capability |
| G01S (radar) | ICEYE's SAR heritage lives here, and it is not satellite communications. Expect ICEYE's patent record to be radar-heavy and comms-thin — that asymmetry is itself a potential finding for "what does ICEYE add" |
| H01Q (antennas generally) | Too broad. Payload beamforming candidates arrive through H04B 7/18515; the claims decide |
| H04B 7/204 (multiple access) | The scheme says it takes precedence over H04B 7/185, so it would blur the SAT pool. Kept as a watch item: if the pilot shows beam and access innovations matter, add H04B 7/2041 (spot beams) with a logged reason |

## Known risks, to be tested rather than assumed away

- **No code cleanly separates LEO from GEO.** H04B 7/195 (non-synchronous stations) is the closest indicator; orbit class is ultimately a claim-reading decision.
- **Code-based pools are unproven until checked by hand.** Each pool needs its own precision check against the 85% bar, a recall test, and a company check — the pre-pivot pools failed this bar on their first pass, so expect iteration.
- **ICEYE's record may be thin.** A young private company with a radar heritage may have few comms patents; absence of patents is not absence of capability, and the analysis must say so if the data shows it.
- **SpaceX stays opaque.** Patent counts don't measure Starlink's real position: SpaceX holds only 110 patent families in the dataset ([query 30](../../sql/30_spacex_name_counts.sql), 10 November 2026) against 19,488 for Airbus — a trade-secret strategy, not a technology gap. The same invisibility applies to classified defence R&D (which does not patent), to Ukrainian suppliers who file only domestically or not at all, and to foreign suppliers who never file in Ukraine. Patent counts are therefore a floor on capability, never a ceiling; SpaceX remains context, not a benchmark, per the [pivot document](pivot-sovereign-satcom.md).

## What happens next

1. ✅ Accepted 11 November 2026, as amended by the pilot decisions R1–R5 (SEC rebuilt as co-occurrence, ISL folded into SAT as a flag, combined measure primary, free-space optical counted as ISL, description paragraph added to the reading rules).
2. ✅ Done ahead of acceptance, 10 November 2026: name research for the five actors ([review](../../data/interim/satcom_name_review.csv)), peers table built ([query 24](../../sql/24_satcom_peers_30y.sql)), and first pool counts run ([query 32](../../sql/32_pool_census.sql), pre-validation). The sandbox tables expire around the end of December 2026, so this was time-boxed.
3. ⬜ In progress: pilot done ([record](../02-methodology/satcom-validation-plan.md#pilot-results-and-diagnosis-10-november-2026)); the stratified re-test sample and hand-check are next — the full plan is in [satcom-validation-plan.md](../02-methodology/satcom-validation-plan.md).
4. ⬜ These pools now replace OPT/IPR/DCS in [`config/research_parameters.toml`](../../config/research_parameters.toml) and [scope.md](scope.md) in one pass, keeping the consistency tests green; the pre-pivot values stay in the config under `[pre_pivot]` so the archived validation record keeps passing its checks.

## Sources

- [USPTO CPC scheme, H04B (transmission)](https://www.uspto.gov/web/patents/classification/cpc/html/cpc-H04B.html) — all H04B codes above, checked 8 November 2026
- [USPTO CPC scheme, H04W (wireless networks)](https://www.uspto.gov/web/patents/classification/cpc/html/cpc-H04W.html) — H04W 84/06, checked 8 November 2026
- [USPTO CPC scheme, H04K (secret communication, jamming)](https://www.uspto.gov/web/patents/classification/cpc/html/cpc-H04K.html) — H04K 1/00 and 3/20, checked 8 November 2026
- System layers and threat context: [sources.md](../appendices/sources.md#sovereign-satcom-context-post-pivot) and the imported [deep-research report](../appendices/deep-research-ukraine-satcom.md) (status-tagged source leads, not verified project facts)
