# AI and cloud networking: who leads?

No single company leads. The leader changes by segment, and Nokia's strongest public positions are in optical.

![No single company leads AI and cloud networking](img/ai_cloud_leaders.png)

## Segment figures behind the map

| Segment | Figures | Source |
|---|---|---|
| Optical transport, 2025 | Huawei, Ciena, Nokia, ZTE, Cisco, in that order | [SDxCentral, reporting Dell'Oro](https://www.sdxcentral.com/news/huawei-ciena-and-nokia-lead-16b-optical-transport-rebound-as-dci-surges/) |
| Data centre interconnect, 2025 | Ciena, Nokia and Cisco in the top three | [SDxCentral, reporting Dell'Oro](https://www.sdxcentral.com/news/huawei-ciena-and-nokia-lead-16b-optical-transport-rebound-as-dci-surges/) |
| Ciena's #1 in interconnect | Its own claim, excluding China | [Ciena investor presentation](https://www.sec.gov/Archives/edgar/data/0000936395/000162828026040614/ex9922026q2earningsprese.htm) |
| Routers, 2Q 2026 | Cisco 34.7%, Huawei 29.9% | [IDC](https://www.idc.com/resource-center/blog/ethernet-switch-market-surges-43-4-to-18-9b-in-2q26-as-ai-infrastructure-demand-drives-record-datacenter-spending/) |
| All Ethernet switching, 2Q 2026 | Cisco 28.7%, Arista 13.4%, Huawei 8.2% | [IDC](https://www.idc.com/resource-center/blog/ethernet-switch-market-surges-43-4-to-18-9b-in-2q26-as-ai-infrastructure-demand-drives-record-datacenter-spending/) |
| Data centre Ethernet, 2Q 2026 | NVIDIA 20.4%, Arista 18.7%, Cisco 18.2% | [IDC](https://www.idc.com/resource-center/blog/ethernet-switch-market-surges-43-4-to-18-9b-in-2q26-as-ai-infrastructure-demand-drives-record-datacenter-spending/) |
| Ethernet AI back-end, 2Q 2026 | Celestica, NVIDIA, Arista, Cisco, in that order | [Dell'Oro](https://www.delloro.com/news/ai-back-end-networks-switch-sales-surpass-front-end-networks-for-the-first-time-in-2q2026/) |

## How fast is each company growing in AI and cloud?

**What this measures:** each company's latest sales in the area, against **its own sales a year earlier**. It shows momentum within a company, not who is bigger, because each company defines its figure differently.

| Company | What's counted | Period | Sales | Change on a year earlier | Source |
|---|---|---|---:|---:|---|
| **Nokia** | Sales to AI and cloud customers | July–September 2026 | €631M | +126% reported, +123% at constant currency | [Nokia Q3 report](https://www.sec.gov/Archives/edgar/data/924613/000110465926117972/tm2628115d1_6k.htm) |
| **Ciena** | Sales to cloud providers | Fiscal Q3 2026 | About $885M (53% of [$1.67B](https://www.sec.gov/Archives/edgar/data/936395/000162828026060245/ex9912026q3earningspressre.htm)) | +82% | [Ciena presentation](https://s25.q4cdn.com/550667411/files/content_files/Ex-99-2-2026-Q3-Earnings-Presentation_FINAL-1.pdf) |
| **NVIDIA** | Ethernet switch sales | April–June 2026 | $2.5B | +181.1% | [IDC](https://www.idc.com/resource-center/blog/ethernet-switch-market-surges-43-4-to-18-9b-in-2q26-as-ai-infrastructure-demand-drives-record-datacenter-spending/) |
| **Arista** | Ethernet switch sales, about 91% data centre | April–June 2026 | $2.5B | +37.6% | [IDC](https://www.idc.com/resource-center/blog/ethernet-switch-market-surges-43-4-to-18-9b-in-2q26-as-ai-infrastructure-demand-drives-record-datacenter-spending/) |
| **Cisco** | AI infrastructure sales | Full fiscal 2026 | About $4B | Not in the source I checked | [Cisco Q4 results](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m08/cisco-reports-fourth-quarter-earnings.html) |

Cisco's row covers a full year, while the others cover one quarter, so its sales can't be compared with theirs directly.

**What it shows:** Nokia's growth is high, partly because it starts from a smaller base of about €279M, which I calculated from its reported growth. Its AI and cloud sales are about 12% of [group sales of €5,154M](https://www.sec.gov/Archives/edgar/data/924613/000110465926117972/tm2628115d1_6k.htm).

**Other figures:** Nokia took [€1.5B of AI and cloud orders](https://www.sec.gov/Archives/edgar/data/924613/000110465926117972/tm2628115d1_6k.htm) in the quarter, with order intake up 118%. Cisco took [$9.3B of AI infrastructure orders](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m08/cisco-reports-fourth-quarter-earnings.html) in fiscal 2026. Arista's whole-company revenue was [$3.036B, up 37.7%](https://www.arista.com/company/news/press-release/24401-pr-20260804).

## Sanity check of the draft analysis

I checked a draft competitor summary from another AI tool against its sources. [All 18 claims are logged](../data/processed/competitor_claims_check.csv).

| Result | Claims | Notes |
|---|---:|---|
| Confirmed in a primary or original source | 14 | Includes all the IDC share figures I checked |
| Trade report of Dell'Oro | 2 | Full Dell'Oro reports are paid, so these rely on secondary coverage |
| Company's own claim | 1 | Ciena's #1 in data centre interconnect, which excludes China |
| Wrong label | 1 | $2.5B and 37.6% are Arista's switch revenue, not its total revenue |

**Other problems with the draft:**

- **It left out the AI back-end leader.** Dell'Oro puts Celestica first and NVIDIA second in Ethernet AI back-end switching.
- **Periods don't line up.** Company fiscal periods and market data cover different dates.
- **The lessons were opinion.** Its statements on what Nokia should learn from each rival are hypotheses to test, not findings.
- **"Nokia is not necessarily losing" isn't established.** Growth rates alone can't show that, and patents haven't been compared yet.

## Comparison set

| Role | Companies | Why |
|---|---|---|
| **Core** | Ciena, Cisco, Arista | Optical, overall networking and data centre focus |
| **Global benchmark** | Huawei | Largest in optical transport, second in routers, with different market exposure |
| **Adjacent** | NVIDIA, Celestica | Lead AI networking segments, but differ from Nokia's portfolio |

## What this can't tell me

Market share shows who sells the most. It doesn't show who holds the strongest patents, so the next step is to test that using the [research design](research-design.md).
