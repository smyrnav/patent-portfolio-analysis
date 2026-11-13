# Technology classification codebook

Version 1.1. It defines what counts as optical networking, IP routing or data-centre switching, so comparisons with competitors aren't caused by inconsistent labels. Whether these labels and codes can be trusted is covered in [validation](validation.md).

**Post-pivot note, 11 November 2026:** the project now works on satellite communications. Version 1.1 stays frozen as the rules of the archived pre-pivot label record; the new satcom classes are [below](#satcom-classes-post-pivot) as version 2.0-draft, and they become 2.0 when the [satcom validation plan](satcom-validation-plan.md) freezes them.

Its starting point was a software-assisted draft. The changes are [listed below](#what-i-changed-from-the-draft).

## Satcom classes (post-pivot)

**Status: version 2.0, frozen 13 November 2026.** Defines what counts as which satellite-communications capability. The code pools that find candidates live in [satcom-code-pools.md](../01-research-design/satcom-code-pools.md), including the CPC prefixes and the SEC co-occurrence rule. Trust status is tracked in the [satcom validation plan](satcom-validation-plan.md): pools are accepted but not yet validated.

| `primary_class` | What the invention mainly does |
|---|---|
| **SAT:** Satellite payload | Communications equipment on the satellite itself: transponders, payloads, on-board processing and beamforming |
| **ISL:** Inter-satellite links | Moving traffic between satellites, radio or optical. A reporting flag inside SAT, not a standalone bucket. Free-space optical terminal patents count here by code definition, even when their sentences never say "satellite" |
| **GRD:** Ground segment and terminals | Gateways, earth stations, network operations and user terminals |
| **NET:** Network integration | Interworking between satellites and terrestrial networks: 3GPP non-terrestrial networks, handover, routing and resource management across the two |
| **SEC:** Security and resilience | Protecting satellite communications: encryption and key management for satellite links, anti-jamming, geofencing, preventing unauthorised access |
| **OTHER** | None of the above — including terrestrial-only wireless and non-communications space technology |
| **MULTI** | The numbered sentences genuinely cover two classes and they can't be separated |

Decision rules, in order: read the independent claims, then the first paragraph of the description (real satellite patents often open with deliberately broad sentences — pilot rule R3), then the rest of the description for context. Titles and CPC codes aren't evidence. Where a patent is used doesn't set its class; what the invention does sets it.

## Primary classes (pre-pivot, archived)

| `primary_class` | What the invention mainly does | Maps to Nokia unit | CPC codes used to find candidates |
|---|---|---|---|
| **OPT:** Optical networking | Transmits, receives, multiplexes or switches optical signals | Optical Networks | H04B 10, H04J 14, H04Q 11/00 |
| **IPR:** IP routing | Calculates, selects, maintains or distributes packet routes | IP Networks | H04L 45 |
| **DCS:** Data-centre switching | Switches packets inside a device or fabric, including its queues, buffers and scheduling | IP Networks | H04L 49 |
| **OTHER** | None of the above | N/A | N/A |
| **MULTI** | The claims genuinely cover two classes, and they can't be separated | N/A | N/A |

CPC codes are only a search tool: they find patents that are *probably* about a topic, but what a patent is really about is decided by reading its claims. H04L 47 is broad traffic control and [failed the pilot](validation.md#pilot-result), and H04L 12 and G02B 6 are too broad to use without another indicator.

MULTI describes the invention, not my uncertainty. A record that's simply unclear gets a low `confidence` and stays in review.

## Decision rules

Read the independent claims first, then the abstract and description for context. Titles and CPC codes aren't evidence.

| Rule | If the main contribution is about | Class |
|---|---|---|
| 1 | Optical signals, components, wavelengths or photonic switching | OPT |
| 2 | Where a packet should go, or how routes are calculated and shared | IPR |
| 3 | Switch devices, fabrics or fabric topology, or queues, buffers and scheduling inside a claimed switch, router or NIC | DCS |
| 4 | None of these | OTHER |
| 5 | Two classes that truly can't be separated | MULTI |

Where a patent is used doesn't set its class. A routing patent for data centres is still IPR.

**Boundary rules from the pilot:**

| Case | Class |
|---|---|
| Management or control of equipment, where the claim adds an optical setting such as launch power or dispersion | OPT |
| Management or control that computes paths or restoration routes | IPR |
| Any other management, control-plane, monitoring or policy claim | OTHER, even if it manages switches or optical equipment |
| Routing of optical signals that depends on wavelengths or optical packets | OPT |
| Path computation that doesn't depend on the optical layer | IPR |
| Traffic control with no switch, router or NIC claimed | OTHER |
| Overlay or VPN forwarding, unless a switch device or NIC pipeline is claimed | OTHER |
| Coherent receiver or transmitter, even if the first claim doesn't say "optical" | OPT |

## Review fields

| Field | Values | Why |
|---|---|---|
| `review_status` | `pending`, `adjudicated`, `accepted` | Pending is a software-generated first-pass label. Adjudicated means a human reviewer resolved a disagreement with that first pass. Accepted means a human reviewer confirmed it |
| `confidence` | High, Medium, Low | Shows which labels are weak |
| `claim_evidence` | Short quote or claim summary | Makes each label checkable |
| `annotator` | Who labelled it | Distinguishes a software-generated first pass from human review without changing the saved values |
| `codebook_version` | For example 1.1 | Ties each label to these rules |

## Secondary fields

| Field | Values | Why |
|---|---|---|
| `dc_context` | 0 or 1 | Explicitly concerns data centres, cloud or HPC |
| `optical_medium` | 0 or 1 | Optical technology is involved |
| `ai_cloud_relevance` | 0 none, 1 possible, 2 explicit | Stops a general telecoms patent counting as an AI infrastructure patent |

OTHER labels with `optical_medium` = 1 stay visible, because optical control software may still matter to the Optical Networks unit.

## Version history

| Version | Change | Why |
|---|---|---|
| 0.1 | Draft rules | Starting point, from a software-assisted draft, with [my changes](#what-i-changed-from-the-draft) |
| 1.0 | Management and control claims no longer go to REVIEW | 8 of the 9 REVIEW labels in the pilot were this case, and REVIEW would have become a dumping ground |
| 1.0 | Scheduling and queues count as DCS only inside a claimed device | Timeslot and traffic policy claims were being pulled in |
| 1.0 | H04L 47 dropped from the DCS candidates | 1 of 19 matched in the pilot |
| 1.1 | REVIEW renamed MULTI, and `review_status` added | Separates overlapping inventions from records awaiting review |
| 2.0 | Satcom classes SAT, ISL, GRD, NET, SEC added; description paragraph added to the reading rules (R3); free-space optical counts as ISL by code definition (R4) | Post-pivot. Accepted with the pilot decisions R1–R5 on 11 November 2026; frozen 13 November 2026 |

Version 1.1 changes names and fields, not rules. All 421 labels were assigned under version 1.0 and carried across mechanically, and no OPT, IPR or DCS label moved, so no re-test was needed. Further rule changes need a logged reason and a re-test.

## What I changed from the draft

| Draft | Problem | My version |
|---|---|---|
| Don't rely on Google's table, as its data dates to 2018 | Not true of this table: it was last modified on 23 September 2026, with filings to August 2026 | Keep Google, and PATSTAT stays optional |
| Two independent annotators | I'm the only human labeler, so whether two people would label the same patent the same way can't be measured — there is no second person to compare against | Human hand-labelling of 100 families per primary category (300 total), a repeated subset for self-consistency (do I agree with my own earlier labels?), and separately reported human–software agreement |
| 300 families straight away | Hand-reading 300 patents is 50–100 hours of one person's time; if the labelling rules turn out to be broken, all of it gets redone | 90-slot pilot first (a day and a half) to break the rules cheaply, then the 300-family human-label target |
| 16 examples as a boundary test | None came from Arista, and few from Nokia or Cisco. Others came from Tigera and Quanta, which aren't in my comparison set | Sample by company |
| Started sampling before building a competitor set | The sample couldn't reflect each company | Build the competitor table first |
| Precision only, with recall as a note | Pools could miss a company's patents | Added a recall test and a company check |
| H04L 12 and G02B 6 as starting codes | Too broad | Not used alone |
| Three labels with no link to the question | Doesn't connect to the business | Mapped to Nokia's units, and added AI and cloud relevance |
