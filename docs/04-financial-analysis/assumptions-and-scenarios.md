# Assumptions and scenarios

What the analysis takes as given, separated into verified inputs and hypothetical assumptions. **Impact** is my estimate of how much an assumption could change the recommendation, and it needs testing.

## Verified inputs

| Input | Value | Basis |
|---|---|---|
| US large-entity renewal fees | $2,150, $4,040, $8,280 | [Official schedule](../appendices/sources.md#patent-rules-and-data-sources), recheck before use |
| US renewal dates | 3.5, 7.5 and 11.5 years after grant | [USPTO](https://www.uspto.gov/patents/maintain) |
| US term | Generally 20 years from filing | [35 U.S.C. § 154](https://www.law.cornell.edu/uscode/text/35/154) |
| US time to grant | Median 4.05 years, mean 4.27 | [Measured](../02-methodology/metrics.md#measured-so-far) from my data |
| Applications per family with grant evidence | Mean 3.68, median 3 | [Measured](../02-methodology/metrics.md#measured-so-far), and known to be low |
| Code pool precision | Optical 73%, routing 39%, switching 42% | [Measured](../02-methodology/validation.md#precision-result) on first-pass labels |

## Top priorities to test

1. **P1:** which patents are still in force and held by Nokia
2. **T1:** whether my labels hold up under human review
3. **V1:** how patent value is distributed, since keep-or-drop depends on it
4. **C1:** fees are paid per national right, while most counts are families
5. **C3:** how many offices each family keeps paying for

## Hypothetical assumptions

### Portfolio: what is being paid for?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| P1 | Candidate families are in force and held by Nokia | 19,873 with grant evidence, 5,595 with a recent application and no grant detected | All costs | High | USPTO renewal and assignment records | **Contradicted in part.** [42 of 179 sampled patents show another assignee](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) |
| P2 | Applicant names find the candidate universe | [Name patterns](../../sql/06_create_portfolio_30y.sql) | Universe size | High | Register spot-check | Partly tested. Japan needed a family lookup |
| P3 | Grant is detected from grant date or kind code | [Rules](../02-methodology/candidate-portfolio-universe.md#how-the-rules-work) | Universe size | Medium | Spot-check by office | Partly tested. Grants outside the US look undercounted |
| P4 | Protection ends 20 years after filing | Cut-off of 1 November 2006 | Expiry and forecast | Medium | Compare with register dates | Not tested. US rule, applied as an approximation elsewhere |
| P5 | Filings since 2021 with no grant detected remain unverified | 1 January 2021 | Filing and grant forecast | Low | Sample register status | Not tested; no detected grant isn't proof of pending status |
| P6 | Families are the unit for inventions | Simple families | Inventions and value | Medium | Compare with extended families | Supported. New families [follow Nokia's reported inventions](../03-market-and-patent-analysis/twenty-years.md#my-family-counts-follow-nokias-own-numbers) |
| P7 | The US, Europe, China and Japan are the offices that matter | Four offices | Scope of the model | Medium | Check filing share in other offices | Chosen, not tested |

### Technology: what counts as AI and cloud networking?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| T1 | [Codebook labels](../02-methodology/classification-codebook.md) separate the three categories reliably | Version 1.1 | All comparisons | High | Agreement test | Not tested. First-pass labels only |
| T2 | CPC codes find most relevant families | H04B 10, H04J 14, H04Q 11/00, H04L 45, H04L 49 | Share and growth | High | Recall test | Not tested. [Precision failed](../02-methodology/validation.md#precision-result) |
| T3 | Optical, routing and switching represent AI and cloud infrastructure | Three categories | The central question | High | Use `ai_cloud_relevance` | Weak so far: 1 explicit AI patent in the 343 tested |

### Costs: what would it cost?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| C1 | Costs can be built per national right, then linked to families | Not modelled | All costs | High | Build the model at right level | Model not started |
| C3 | Number of offices maintained per family | Filed in a mean of 3.43 offices, median 3, including international filings | Geography scenario | High | Renewal data where possible | Filing measured, maintained offices unknown |
| C4 | European renewal costs after grant | Not set | Europe costs | High | National fees and typical countries | Not started |
| C5 | Chinese and Japanese fees | Not set | China and Japan costs | Medium | Official schedules | Not started |
| C7 | Fee growth and exchange rates | Not set | Forecast | Medium | Fee history and sensitivity test | Not started |

Filing, attorney and translation costs are [outside the statutory baseline](ten-year-maintenance-cost-model.md#modelling-rules).

### Behaviour: what happens next?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| F1 | Renewal rates at 3.5, 7.5 and 11.5 years | Placeholders of 90/80/70% and 80/60/40% | Mean, median and forecast | High | USPTO renewal records | Placeholder |
| F2 | Renewal rates vary by age, origin and technology | Not set | Keep-or-drop and scenarios | High | Split renewal rates | Not started |
| F3 | Future new inventions per year | Not set | Filing volumes and capacity | Medium | Scenarios from the [recent trend](../03-market-and-patent-analysis/twenty-years.md) | Not started. Recent data is provisional |
| F4 | Past behaviour predicts future choices | Not set | Forecast | Medium | Compare periods | Not started |

### Value: what is it worth?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| V1 | How value is spread across families | Not set | Keep-or-drop | High | Scenarios, then proxies | Real split isn't public |
| V2 | Discount rate | 5%, 10%, 15% | Present value and break-even | Medium | Sensitivity test | Tested for the [break-even example](us-renewal-break-even.md) only |
| V3 | Renewals, citations, breadth and declarations indicate value | Not set | Keep-or-drop shortlist | High | Check whether indicators agree | Not tested, and these aren't proof of value |
| V5 | ETSI declarations indicate standards relevance | Not collected | Which patents to protect | Medium | Compare with family data | Parked. ETSI doesn't verify essentiality |

### Budget: what would the company do with this?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| B1 | The budget is limited and can be moved between activities | Assumed | The whole question | High | Ask the team if I get the chance | Assumed |
| B3 | Dropping low-signal patents wouldn't harm licensing | Not set | Savings against risk | High | State the risk, and test the shortlist against declarations | Not tested |
| B4 | Costs can be allocated to business units | Not set | Scenarios | Medium | State a rule for families serving several units | Not started |
| B5 | Team capacity per task | Not set | Capacity plan | Low | Assumed hours as ranges | Not started |

**Retired:** B2 and V4 used fees as a share of licensing sales, and sales per family, as a sense of scale. Those ratios don't establish efficiency or value, so [I removed them](../appendices/research-log.md#repository-review-november-2026).

## Scenarios

There are two sets, and they answer different questions.

| Set | Question | Options |
|---|---|---|
| **Maintenance scenarios (RQ4)** | What would a defined set of rights cost? | [A Maintain, B Selective maintenance, C Optimisation](ten-year-maintenance-cost-model.md#scenarios) |
| **Investment strategies (RQ5)** | Where should patent investment go? | Below |

| Strategy | What changes | What I'd compare |
|---|---|---|
| **Maintain** | Continue the current filing and renewal approach | Highest cost, least risk of dropping something valuable |
| **Concentrate** | Move spending from older areas to optical, routing or switching gaps | New filing costs against cover given up |
| **Optimise** | Reallocate through selective filing, geography and renewals | Savings against lost market cover |

Sensitivity then tests renewal rates, fee growth, exchange rates and the discount rate.

## Capacity plan

Volumes of filings and renewal decisions come from the forecast, and hours per task are assumptions, shown as ranges. Not started, and only worth building once the forecast exists.

## Finance concepts in this project

| Concept | What it means here |
|---|---|
| **CAPEX vs OPEX** | Whether patent costs are recorded as a long-term asset or an expense. I don't know how Nokia treats each cost, so I'll model cash spending and flag this as a question |
| **Budget vs actuals** | Planned against actual spend. I can build the planning side, but actuals are internal |
| **Cost allocation** | Assigning costs to business units, offices and technologies. One family can serve several units, so the rule needs to be stated |
| **Cost drivers** | Number of rights, offices per invention, patent age, fee levels and exchange rates |
| **ROI** | Return compared with cost. It needs a value for each patent, which has to be an assumption |
| **NPV** | Future value and costs converted to today's money. Used for keep-or-drop |
| **Discount rate** | How much less future money is worth today. I test a range because I don't know Nokia's rate |
| **Forecasting** | Estimating renewals and new filings by year |
| **Sensitivity analysis** | Changing one assumption at a time |
| **Scenario analysis** | Changing several assumptions together to compare futures |

## What this could offer, if the tests hold up

- A method for estimating statutory maintenance costs, as a range
- A public-data shortlist of areas to review, not patents to drop
- A view of which assumptions most change the cost

What it can't give without internal data: actual savings, the value of a patent or a final keep-or-drop decision.
