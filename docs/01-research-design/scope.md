# Scope, version 2.0

All documents use this scope, and [`config/research_parameters.toml`](../../config/research_parameters.toml) holds the same values for the scripts.

**Changed 11 November 2026:** version 1.0 covered optical networking, IP routing and data-centre switching (OPT, IPR, DCS) against Ciena, Cisco, Arista and Huawei. The project pivoted to sovereign satellite communications; version 1.0 survives as the archived pre-pivot record under `[pre_pivot]` in the config and in the [codebook's frozen section](../02-methodology/classification-codebook.md).

**Re-aimed 24 November 2026:** the [central question](research-design.md#central-research-question) changed; the technology pools, companies, offices and dates below are unchanged.

## Technology

Five pools, defined in [satcom-code-pools.md](satcom-code-pools.md) (accepted 11 November 2026, amended by pilot decisions R1–R5, not yet validated). The **combined satcom capability pool — a family in any of the five — is the primary comparative measure**, because the pilot showed the main defect is patents landing in the wrong sub-bucket, not non-satellite junk.

| Pool | Definition |
|---|---|
| **SAT:** Satellite payload | Communications equipment on the satellite: transponders, payloads, on-board processing and beamforming |
| **ISL:** Inter-satellite links | Moving traffic between satellites, radio or optical. A reporting flag inside SAT, not a standalone bucket |
| **GRD:** Ground segment and terminals | Gateways, earth stations, network operations and user terminals |
| **NET:** Network integration | Interworking between satellites and terrestrial networks (3GPP non-terrestrial networks, handover, routing) |
| **SEC:** Security and resilience | Protecting satellite communications: encryption and key management for satellite links, anti-jamming, geofencing, access prevention. Found by co-occurrence of a satellite code and a security code |

The exact labelling rules are in the [codebook](../02-methodology/classification-codebook.md#satcom-classes-post-pivot).

**Taxonomy status, updated 24 November 2026.** ISL is a code-defined reporting tag inside SAT (pilot decision R5), not a standalone comparative bucket; it appears in the label lists only so sampling and reporting can tag it. SEC is the co-occurrence rule above; [query 32](../../sql/32_pool_census.sql) initially implemented it differently (security codes alone) and was corrected on 24 November 2026 — the saved SEC census rows predate that correction. GRD and SEC had effectively no validation sample (one observation each on 13 November), so no pool-specific comparison may use them. The next taxonomy redesign will separate **primary capability** (what the invention does) from **technology attributes** (inter-satellite link, optical, anti-jamming, encryption). Until then, the combined satcom pool remains the only comparative measure.

## Companies

| Role | Companies | How they're used |
|---|---|---|
| **Reference** | Nokia | Measured in all five pools, plus the combined measure |
| **Core comparators** | Airbus, Thales, Viasat, Eutelsat/OneWeb | Incumbent satellite and defence suppliers. Their dataset-wide portfolios are large; their satcom-specific shares are unvalidated until the pools pass |
| **Partner, measured like a comparator** | ICEYE | Read as a complement to Nokia, not a rival. Its small comms-pool count is a preliminary, classification-level result |
| **Context, not a benchmark** | SpaceX | The dominant actor, with 110 name-matched families. Patent counts cannot measure its position, so it is never benchmarked here |

Matching is exact-name, post-census, per actor: the name research is in [`data/interim/satcom_name_review.csv`](../../data/interim/satcom_name_review.csv), with 11 names still awaiting a keep/drop decision.

## Patent offices and dates

| Item | Value | Why |
|---|---|---|
| Filings | Since 1 November 1996 | Covers anything that could still be in term, plus 10 years of history |
| Could still be in term | Filed since 1 November 2006 | About 20 years from filing, as an approximation |
| Recent application with no grant detected | No grant evidence, filed since 1 January 2021 | Saved-data label, not proof of pending or register status |
| Main comparison period | 2020–2024 | Filing years with mostly complete publication |
| Provisional years | 2025–2026 | Publication lags filing by about 18 months |

## Units

| Unit | Used for |
|---|---|
| **Simple patent family** | Counting inventions and comparing technology positions |
| **Individual national right** | Renewal fees, because fees are paid per right, not per family |

## Parked

These extensions use the same method, and only start if the main question is answered. Their draft hypotheses (H5–H8) live in git history; none is active.

| Extension | Why it's parked |
|---|---|
| AI-RAN and 6G capability map | "6G" and "AI-native" have no settled patent classification |
| Licensing opportunity database | Public sources can't show who is already licensed |
| ETSI declarations | Not needed for the current pool comparison |
| Other Nokia business units | Outside the central question |
