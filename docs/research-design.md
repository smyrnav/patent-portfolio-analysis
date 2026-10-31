# Research design

Metrics only matter if they can change a decision. This page sets the three questions, what would count as an answer and how reliable each answer can be from public data. I fix these rules before seeing the results.

## What each priority can deliver

| Priority | Decision it informs | Deliverable | Achievable reliability |
|---|---|---|---|
| **1. AI and cloud infrastructure** | Where to direct optical and IP patent and R&D spending | Technology gap map and R&D opportunity analysis | **Medium to high** for patent position, not for commercial return |
| **2. AI-RAN and 6G** | Which capabilities to build, partner on or watch | Strategic technology capability map | **Low to medium**, as the field is young and classification is harder |
| **3. Licensing opportunities** | Which areas and companies deserve a closer commercial look | Public-source opportunity database | **Medium** for patents, **low** for who is already licensed |

**Order:** Priority 1 first, as it has the cleanest data and connects to [Nokia's reported growth](sources.md#nokias-business-structure). Priorities 2 and 3 use the same method if Priority 1 passes its checks.

All three feed the [budget question](strategy.md): each ends by saying what it would change about where money goes.

## Priority 1: AI and cloud infrastructure

**Question:** does Nokia's patent position in optical and IP networking support its growth, and where are the gaps?

| Hypothesis | Measure | What would disprove it |
|---|---|---|
| H1: Infinera materially strengthened Nokia's optical position | Optical families and share, with and without Infinera | Infinera adds little in key optical areas, or mostly duplicates Nokia's cover |
| H2: Nokia's IP position trails the leaders in data centre networking | Share of new families in routing and switching, 2020–2024 | Nokia's share is level with or above the leading rivals' |
| H3: Part of Nokia's cover is ageing without enough replacement | Families reaching 20 years by 2036, against new families | New families outnumber expiring ones in each area |
| H4: Cover in the main markets has gaps | Share of families in the US, Europe, China and Japan, against rivals | Coverage matches rivals' in each market |

**Comparison set:** to be confirmed against company reports, starting with Ciena, Cisco, Huawei, Arista, Juniper and ZTE. Owner names need the same cleaning I used for Nokia, and deals such as Cisco's Acacia must be handled explicitly.

**Output:** a heatmap of technology areas against companies, showing share and growth, then a short list of gaps ranked by size, confidence and link to the business.

## Priority 2: AI-RAN and 6G

**Question:** where does Nokia hold a strong position in AI-native networks and 6G, and where does it depend on others?

| Hypothesis | Measure | What would disprove it |
|---|---|---|
| H5: Nokia has a leading position in RAN automation | Share of families matched to a tested definition | Share isn't in the top group |
| H6: Partners hold important capabilities Nokia lacks | Comparison of technology areas across partners | Partner areas mostly overlap with Nokia's |

**Main risks:** "6G" and "AI-native" have no settled patent classification, so the set relies on keywords and text. Recent filings are incomplete, and 6G filings may be too few to rank. Partners also need to be sourced from public announcements.

**Rule:** if a definition fails the checks below, I report that the data can't support a ranking.

## Priority 3: Licensing opportunities

**Question:** which technology areas and implementers deserve a closer commercial look?

| Hypothesis | Measure | What would disprove it |
|---|---|---|
| H7: Multimedia and non-smartphone areas have room to grow | Declared and multimedia families, against public deal coverage | Public sources show those markets are already widely licensed |
| H8: Nokia's declared families have long enough life to support licensing | Remaining years by standard | Most declared families expire soon |

**What the database can contain:** company, sector, the relevant standards, public evidence of use, known licence status, source link and date.

**What it can't contain:** confidential licence terms, or a claim that a company infringes or needs a licence. "No public licence found" doesn't mean unlicensed. Legal review would be needed before any use.

## How I keep answers reliable

Every finding has to pass these checks:

| Check | Pass rule |
|---|---|
| **Classification** | Hand-label a random 100 families per area, with precision of at least 80% |
| **Owner matching** | Review the top names for each company, and spot-check a sample against registers |
| **Robustness** | Same direction under a second technology definition |
| **Unit** | Same direction in families and in US grants |
| **Time** | Use 2020–2024 as the main period, and treat 2025–2026 as provisional |
| **Independent check** | Compare with company reports or other outside evidence |

These thresholds are my own working standards, not an industry rule.

## How to state an answer

Each finding uses this format:

1. **Answer:** one sentence
2. **Evidence:** the numbers and sources
3. **Confidence:** high, medium or low, with the reason
4. **What would change it:** the result or data that would overturn it
5. **Decision:** what to do, investigate or stop doing

## Rules that stop endless metric-pulling

- Each query must test a named hypothesis.
- A chart only goes in if it supports, disproves or qualifies one.
- Each priority ends with at most five findings, and a stated decision for each.
- "The data can't answer this" is a valid result.
- When a decision wouldn't change with more data, the analysis stops.

## What public data can't settle

Patents show technical position, not product quality or market share. Citations and family counts are indicators rather than value. A final R&D or licensing decision also needs Nokia's internal costs, roadmaps and deals.

## Data needed

| Data | Priority | Status |
|---|---|---|
| Rival patent table | 1, 2 | Not built. Check the query size first, and use only the columns needed |
| Business unit technology definitions | 1, 2, 3 | Draft only, to be tested |
| USPTO renewal and assignment records | 1, 3 | Needs a USPTO account |
| ETSI declarations | 2, 3 | Free to export, not done yet |
| Public licence announcements and partner lists | 2, 3 | Not collected |
