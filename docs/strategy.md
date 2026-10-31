# Analysis strategy

I started by following whatever the data showed next. I then set out business questions, and now I've focused the project on the [Business Data Analytics track](#the-role-this-project-targets) of the role that caught my eye. [Here's how my approach changed](approach-changes.md).

This is an outside view. It uses public data and clearly labelled assumptions, not Nokia's internal figures.

This work follows the posting's [expectations for how people work](principles.md). The priority questions and their reliability rules are in the [research design](research-design.md).

## The central research question

> How does Nokia's patent portfolio and associated investment position compare with the leading competitors in AI and cloud infrastructure networking, and what strategic and financial lessons can be identified?

The financial side comes down to one problem: with a limited patent budget, how should it be allocated to get the most strategic and economic value?

The budget has to cover:

- New patent applications
- Maintaining existing patents
- Different geographical markets
- Different technology areas
- External patent services
- Portfolio management resources

## The role this project targets

The [Financial Data Engineering / Business Data Analytics Trainee posting](https://www.linkedin.com/jobs/view/4483030441) at Nokia, in the Business Data Analytics track.

| What the role does | What I'll build |
|---|---|
| Analyse patent portfolio and financial data | Portfolio volumes linked to fee and cost data |
| Investment modelling | A cost forecast, and NPV for keep-or-drop decisions |
| Cost-efficiency studies | Cost per invention by office and technology, and what drives it |
| Scenario analysis | Three budget scenarios, compared side by side |
| Business cases | One recommendation with costs, benefits and risks |
| Demand and capacity planning | Forecast filings and renewals against a team's capacity |
| Presenting findings and reliability | A one-page brief showing ranges, assumptions and data limits |

## The deliverables

### 1. Baseline cost forecast

**Question:** what would the current portfolio cost to keep over the next 10 years?

Patent volumes come from my [filtered portfolio](portfolio-filter.md), for the US, Europe, China and Japan. Fees come from official schedules. Internal costs are assumptions, labelled as such.

### 2. Keep-or-drop model

**Question:** how much value must a patent generate to justify its next renewal fee?

A worked example using the [USPTO large-entity fees](sources.md#patent-rules-and-data-sources), and the [median US time to grant of 4.05 years](../data/processed/patent_measures.csv):

| Renewal | Fee | Cover it buys | Break-even value per year at 5% | At 10% | At 15% |
|---|---:|---:|---:|---:|---:|
| 3.5 years | $2,150 | 4 years | $606 | $678 | $753 |
| 7.5 years | $4,040 | 4 years | $1,139 | $1,275 | $1,415 |
| 11.5 years | $8,280 | 4.45 years | $2,121 | $2,395 | $2,682 |

The three fees total $14,470, or about $6,284 in present value at 10%.

The fee rises, but so does the time it buys in this example. The discount rate and the value of each patent are assumptions, because public data doesn't show them.

### Mean and median patent costs

Nokia's reports don't show patent costs, so these need official fees and renewal records. I can't get those records yet, as the [USPTO portal needs an account](data-map.md#whats-missing). This example shows how the calculation works, using assumed renewal rates and today's US large-entity fees:

| Share renewed at 3.5, 7.5 and 11.5 years (assumed) | Mean fees per patent | Median fees per patent |
|---|---:|---:|
| 90%, 80%, 70% | $9,017 | $14,470 |
| 80%, 60%, 40% | $5,249 | $2,150 |

The median can jump a long way with small changes, as fees come in large steps, so the mean and the full spread both matter. These are official renewal fees only, not filing or attorney costs. The rates are placeholders, not findings.

### 3. Three budget scenarios

| Scenario | What changes | What I'd compare |
|---|---|---|
| **Keep everything** | Renew all eligible patents | Highest cost, least risk of dropping something valuable |
| **Narrow the geography** | Maintain fewer offices per invention | Savings against lost market cover |
| **Shift the mix** | Move spending from older areas to priority areas | Savings against new filing costs |

Priority areas can use [Nokia's reported business units](sources.md#nokias-business-structure). IP Networks and Optical Networks are the growth areas in its Q3 2026 report, so they make a good test case.

### 4. Sensitivity analysis

**Question:** which assumptions move the answer most?

I'll test the renewal rate, fee growth, cost per application, exchange rates, and the discount rate, then show the results in a chart.

### 5. Demand and capacity plan

**Question:** how many filings and renewal decisions will the team handle each year, and is that within capacity?

Volumes come from the forecast. Hours per task are assumptions.

### 6. Decision brief

One page with the recommendation, savings range, risks and how reliable each number is.

## Early answer: are fees big enough to matter?

A rough check for official US renewal fees: if 1,000–1,300 US patents a year were each kept for their full term, fees would reach about **$14.5M–$18.8M a year** once the portfolio is steady.

That's about **1% of Nokia's roughly €1.6B annualised licensing-unit sales**, before converting currency. It assumes every patent is renewed, so real fees could be lower.

**What this changes:** cutting renewals alone is unlikely to be the main prize, and a small saving wouldn't justify much licensing risk. The model also needs other offices, filing and attorney costs before it can say where the money goes. This is an order-of-magnitude check, not Nokia's real spend.

## Measured so far

| Measure | Mean | Median | Middle 80% | Patents or families |
|---|---:|---:|---:|---:|
| US years to grant | 4.27 | 4.05 | 2.16–6.66 | 10,855 |
| European years to grant | 6.17 | 5.79 | 2.79–9.92 | 6,417 |
| Chinese years to grant | 4.89 | 4.88 | 3.67–6.08 | 2,278 |
| Applications per core family | 3.68 | 3 | 1–6 | 19,873 |
| Offices per core family, including international filings | 3.43 | 3 | 1–6 | 19,873 |

Time to grant covers filings from November 2006 to 2015, so recent cases don't skew it short. Filings per family are low, because they rely on owner names and miss some records, such as many Japanese ones. Filing somewhere doesn't mean a patent is being maintained there.

## Finance concepts in this project

| Concept | What it means here |
|---|---|
| **CAPEX vs OPEX** | Whether patent costs are recorded as a long-term asset or an expense. I don't know how Nokia treats each cost, so I'll model cash spending and flag this as a question |
| **Budget vs actuals** | Planned against actual spend. I can build the budget side, but actuals are internal |
| **Cost allocation** | Assigning costs to business units, offices and technologies. One family can serve several units, so the rule needs to be stated |
| **Cost drivers** | Number of inventions, offices per invention, patent age, fee levels and exchange rates |
| **ROI** | Return compared with cost. It needs a value for each patent, which has to be an assumption |
| **NPV** | Future value and costs converted to today's money. Used for keep-or-drop |
| **Discount rate** | How much less future money is worth today. I test a range because I don't know Nokia's rate |
| **Forecasting** | Estimating renewals and new filings by year |
| **Sensitivity analysis** | Changing one assumption at a time |
| **Scenario analysis** | Changing several assumptions together to compare futures |

## What each input is based on

| Input | Status |
|---|---|
| Patent counts by office and year | [Filtered](portfolio-filter.md), but lapsed and sold patents aren't removed yet |
| US and European fees | Official, check they're current |
| US renewal behaviour | Public USPTO records, not yet collected |
| European renewal behaviour | Harder to get, needs Espacenet or a PATSTAT trial |
| Application and attorney costs | Assumption |
| Team capacity | Assumption |
| Patent value and discount rate | Assumption, tested as ranges |
| Nokia's real budget, costs and licensing income | Not available |

## Known limits

- **Portfolio size:** my [filter](portfolio-filter.md) reduces 72,207 families to 19,873 granted families within 20 years, plus 5,595 possibly pending. Nokia [reports 26,000+](twenty-years.md). The filter doesn't yet remove patents that lapsed or were sold.
- **Focus offices:** the model covers the US, Europe, China and Japan, with [filings found by family](twenty-years.md#japan-needed-fixing).
- **Trust:** see [how far I trust each part of the data](data-trust.md).
- **Recent years:** publication lags filing by about 18 months, so recent trends are provisional.
- **Patent value:** citations and family size are indicators, not measures of commercial value.

## Rule for each new query

This follows the [working principles](principles.md).

Before running a query, I write down:

1. **Which deliverable** it feeds
2. **The decision** it informs
3. **The measure** I'd use
4. **What result would change my mind**
5. **The main limit** of the data

If it doesn't feed a deliverable, the query doesn't get run.

## The wider questions

Competitive position, AI-RAN and 6G, and licensing are now covered in the [research design](research-design.md), and each one has to say what it changes about the budget.
