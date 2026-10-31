# Assumption register

Every assumption behind the analysis. The final column shows whether I've tested how much it moves the answer.

| # | Assumption | Value | Why | Could change | Tested? |
|---|---|---|---|---|---|
| A1 | Inventions are counted as simple patent families | `family_id` | One invention filed in many offices shouldn't count many times | All counts | No |
| A2 | Owner search finds the portfolio | Name patterns in [the build query](../sql/06_create_portfolio_30y.sql) | Public data has no current-owner field | Portfolio size | Partly, I read the owner names for US filings |
| A3 | A document counts as granted if it has a grant date, or a kind code starting with B, C or E | See [the filter](portfolio-filter.md) | Grant dates are incomplete outside the US | Portfolio size | Partly, Japan and China look undercounted |
| A4 | Protection lasts up to 20 years from filing | Cut-off of 1 November 2006 | [US rule](sources.md#patent-rules-and-data-sources), and used as an approximation for other offices | Portfolio size | No |
| A5 | Ungranted filings since 2021 may be pending | 1 January 2021 | Examination often takes years | Pending count | No |
| A6 | Time from filing to US grant | 3 years | Placeholder for the break-even example | Break-even values | Not yet, can be measured from my data |
| A7 | Discount rate | 5%, 10% and 15% | Nokia's rate isn't known | NPV and break-even | Yes, for the break-even example |
| A8 | US fees are large-entity rates | $2,150, $4,040, $8,280 | [USPTO schedule](sources.md#patent-rules-and-data-sources), to be rechecked | Cost forecast | No |
| A9 | Renewal rates | To be measured | USPTO records | Cost forecast | Not yet |
| A10 | Costs per application and hours per task | To be set | Internal figures aren't public | Forecast and capacity | Not yet |
