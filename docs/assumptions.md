# Assumption register

Every assumption behind the [budget analysis](strategy.md), grouped by the decision it affects. **Impact** is my estimate of how much it could change the recommendation, and it needs testing. **Status** shows what's been done.

## Top priorities to test

1. **V1:** how patent value is distributed, since keep-or-drop depends on it
2. **C1:** fees are paid per national patent, while I count families
3. **P1:** which patents are still alive and owned
4. **C3:** how many offices each family keeps paying for
5. **B2:** whether official fees are large enough to matter compared with other costs

## Portfolio: what is being paid for?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| P1 | Filtered families are live and owned | 19,873 core, 5,595 possibly pending | All costs | High | USPTO renewal and assignment records | Not tested. Lapsed and sold patents remain |
| P2 | Owner names find the portfolio | [Name patterns](../sql/06_create_portfolio_30y.sql) | Portfolio size | High | Register spot-check | Partly tested. Japan needed a family lookup |
| P3 | Grant is detected from grant date or kind code | [Filter rules](portfolio-filter.md) | Portfolio size | Medium | Spot-check by office | Partly tested. Grants outside the US look undercounted |
| P4 | Protection ends 20 years after filing | Cut-off of 1 November 2006 | Expiry and forecast | Medium | Compare with register dates | Not tested. [US rule](sources.md#patent-rules-and-data-sources), applied as an approximation elsewhere |
| P5 | Ungranted filings since 2021 may be pending | 1 January 2021 | Filing and grant forecast | Low | Sample register status | Not tested |
| P6 | Families are the unit for inventions | Simple families | Inventions and value | Medium | Compare with extended families | Supported. New families [follow Nokia's reported inventions](twenty-years.md) |
| P7 | The US, Europe, China and Japan are the offices that matter | Four offices | Scope of the budget | Medium | Check filing share in other offices | Chosen, not tested |

## Costs: what would it cost?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| C1 | Costs can be built per national patent, then linked to families | Not modelled. Core families average 3.68 applications | All costs | High | Build the model at patent level | [Measured](../data/processed/patent_measures.csv), model not started |
| C2 | Official fees use large-entity rates | US $2,150, $4,040, $8,280 | US costs | Medium | Recheck the schedule | Official, recheck before use |
| C3 | Number of offices maintained per family | Filed in a mean of 3.43 offices, median 3, including international filings | Geography scenario | High | Renewal data where possible | Filing measured, maintained offices not known |
| C4 | European renewal costs after grant | Not set | Europe costs | High | National fees and typical countries | Not started |
| C5 | Chinese and Japanese fees | Not set | China and Japan costs | Medium | Official schedules | Not started |
| C6 | Filing, attorney and translation costs | Not set | New filing costs | High | Public benchmarks, then ranges | Not started. Current surveys are paid |
| C7 | Fee growth and exchange rates | Not set | Forecast | Medium | Fee history and sensitivity test | Not started |
| C8 | US time from filing to grant | Median 4.05 years, mean 4.27 | Break-even example | Low | Measured from my data | Tested. It raised the 11.5-year break-even from $2,030 to $2,395 at 10% |

## Behaviour: what happens next?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| F1 | Renewal rates at 3.5, 7.5 and 11.5 years | Placeholders of 90/80/70% and 80/60/40% | Mean, median and forecast | High | USPTO renewal records | Placeholder |
| F2 | Renewal rates vary by age, origin and technology | Not set | Keep-or-drop and scenarios | High | Split renewal rates | Not started |
| F3 | Future new inventions per year | Not set | Filing budget and capacity | Medium | Scenarios from the [recent trend](twenty-years.md) | Not started. Recent data is provisional |
| F4 | Past behaviour predicts future choices | Not set | Forecast | Medium | Compare periods | Not started |

## Value: what is it worth?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| V1 | How value is spread across families | Illustrative splits only | Keep-or-drop | High | Scenarios, then proxies | Illustrative. Real split isn't public |
| V2 | Discount rate | 5%, 10%, 15% | NPV and break-even | Medium | Sensitivity test | Tested for the break-even example only |
| V3 | Renewals, citations, breadth and declarations indicate value | Not set | Keep-or-drop shortlist | High | Check whether indicators agree with each other | Not tested, and these aren't proof of value |
| V4 | Licensing sales give a sense of scale | About €62k–€82k per family | Scale check | Medium | Use several years | Single-year figure. Sales swing with renewal cycles |
| V5 | ETSI declarations indicate standards relevance | Not collected | Which patents to protect | Medium | Compare with family data | Not started. ETSI doesn't verify essentiality |

## Budget: what would the company do with this?

| # | Assumption | Current value | Affects | Impact | How to test | Status |
|---|---|---|---|---|---|---|
| B1 | The budget is limited and can be moved between activities | Taken from my [strategy](strategy.md) | The whole question | High | Ask the team if I get the chance | Assumed |
| B2 | Official fees are a big enough share to be worth optimising | [About $14.5M–$18.8M a year](strategy.md#early-answer-are-fees-big-enough-to-matter) for US renewals, roughly 1% of licensing-unit sales | Size of savings | High | Add other offices and costs | Rough US check only. Renewal savings alone look small |
| B3 | Dropping low-signal patents wouldn't harm licensing | Not set | Savings against risk | High | State the risk, and test the shortlist for overlap with declarations | Not tested |
| B4 | Costs can be allocated to business units | Not set | Mix scenario | Medium | State a rule for families serving several units | Not started |
| B5 | Team capacity per task | Not set | Capacity plan | Low | Assumed hours as ranges | Not started |

## The value this analysis can offer

What it could give Nokia, if the tests above hold up:

- A method for estimating what the portfolio costs to maintain, as a range
- A public-data shortlist of areas to review, not patents to drop
- A view of which assumptions most change the budget

What it can't give without internal data: the actual savings, the value of a patent or a final keep-or-drop decision.
