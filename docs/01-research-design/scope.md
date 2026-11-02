# Scope, version 1.0

All documents use this scope, and [`config/research_parameters.toml`](../../config/research_parameters.toml) holds the same values for the scripts.

## Technology

| Category | Definition | Primary competitor | Nokia unit |
|---|---|---|---|
| **OPT:** Optical networking | Optical transmission, transport, multiplexing and optical switching | Ciena | Optical Networks |
| **IPR:** IP routing | IP route computation, routing protocols, route selection and forwarding | Cisco | IP Networks |
| **DCS:** Data-centre switching | Packet switching, switching fabrics, buffers, queues and data-centre network architectures | Arista Networks | IP Networks |

The exact rules are in the [codebook](../02-methodology/classification-codebook.md). These three categories are a selected lens on AI and cloud infrastructure, not everything Nokia does in that market. A patent in one of them isn't automatically an AI patent, which is why the codebook also scores [AI and cloud relevance](../02-methodology/classification-codebook.md#secondary-fields).

## Companies

| Role | Companies | How they're used |
|---|---|---|
| **Reference** | Nokia | Measured in all three categories |
| **Core comparators** | Ciena, Cisco, Arista Networks | Each is compared across all three categories, not only its primary one |
| **Supplementary global benchmark** | Huawei | Measured in all three categories, because of its position in optical transport and networking |
| **Commercial and technology context only** | NVIDIA, Celestica | Appear in [market context](../03-market-and-patent-analysis/market-context-and-peer-selection.md), not in patent comparisons |

Acquired names count with the acquirer where the deal is known: Infinera with Nokia, and Acacia and Luxtera with Cisco.

## Patent offices and dates

| Item | Value | Why |
|---|---|---|
| Offices | US, European Patent Office, China, Japan | The main markets. US data is the most complete, so first estimates use US members |
| Filings | Since 1 November 1996 | Covers anything that could still be in term, plus 10 years of history |
| Could still be in term | Filed since 1 November 2006 | About 20 years from filing, as an approximation |
| Recent application with no grant detected | No grant evidence, filed since 1 January 2021 | Saved-data label, not proof of pending or register status |
| Main comparison period | 2020–2024 | Filing years with mostly complete publication |
| Provisional years | 2025–2026 | Publication lags filing by about 18 months |
| Annual reports | FY2006–FY2025 | Twenty years is enough context |

## Units

| Unit | Used for |
|---|---|
| **Simple patent family** | Counting inventions and comparing technology positions |
| **Individual national right** | Renewal fees, because fees are paid per right, not per family |

## Parked

These extensions use the same method, and only start if the main question is answered. Their [hypotheses are recorded](research-questions.md#parked-extensions).

| Extension | Why it's parked |
|---|---|
| AI-RAN and 6G capability map | "6G" and "AI-native" have no settled patent classification |
| Licensing opportunity database | Public sources can't show who is already licensed |
| ETSI declarations | Not needed for the optical, routing and switching comparison |
| Other Nokia business units | Outside the central question |
