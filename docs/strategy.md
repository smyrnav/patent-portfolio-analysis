# Analysis strategy

I started by following whatever the data showed next. I then set out business questions, and now I've focused the project on the [Business Data Analytics track](#the-role-this-project-targets) of the role that caught my eye. [Here's how my approach changed](approach-changes.md).

This is an outside view. It uses public data and clearly labelled assumptions, not Nokia's internal figures.

## The central problem

> Nokia has a limited annual budget for patent portfolio management. How should it be allocated to get the most strategic and economic value from the portfolio?

The budget has to cover:

- New patent applications
- Maintaining existing patents
- Different geographical markets
- Different technology areas
- External patent services
- Portfolio management resources

## The role this project targets

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

Patent volumes come from my [filtered portfolio](portfolio-filter.md), starting with the US and Europe. Fees come from official schedules. Internal costs are assumptions, labelled as such.

### 2. Keep-or-drop model

**Question:** how much value must a patent generate to justify its next renewal fee?

A worked example using the [USPTO large-entity fees](sources.md#patent-rules-and-data-sources), and assuming a patent is granted 3 years after filing:

| Renewal | Fee | Cover it buys | Break-even value per year at 5% | At 10% | At 15% |
|---|---:|---:|---:|---:|---:|
| 3.5 years | $2,150 | 4 years | $606 | $678 | $753 |
| 7.5 years | $4,040 | 4 years | $1,139 | $1,275 | $1,415 |
| 11.5 years | $8,280 | 5.5 years | $1,759 | $2,030 | $2,316 |

The three fees total $14,470, or about $6,284 in present value at 10%.

The fee rises, but so does the time it buys in this example. The real insight will come from applying this across thousands of patents, and from adding other countries' fees. The discount rate and the value of each patent are assumptions, because public data doesn't show them.

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

- **Portfolio size:** my [filter](portfolio-filter.md) reduces 72,207 families to 19,873 granted families within 20 years, plus 5,595 possibly pending. It doesn't yet remove patents that lapsed or were sold.
- **Trust:** see [how far I trust each part of the data](data-trust.md).
- **Recent years:** publication lags filing by about 18 months, so recent trends are provisional.
- **Patent value:** citations and family size are indicators, not measures of commercial value.

## Rule for each new query

Before running a query, I write down:

1. **Which deliverable** it feeds
2. **The decision** it informs
3. **The measure** I'd use
4. **What result would change my mind**
5. **The main limit** of the data

If it doesn't feed a deliverable, the query doesn't get run.

## The wider questions

These are still worth knowing, but they're outside this project for now: competitive intelligence, licensing opportunities, market foresight and AI-RAN or 6G analysis. Rival data and ETSI declarations would be the next additions.
