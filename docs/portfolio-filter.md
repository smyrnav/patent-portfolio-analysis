# The workable portfolio

My table had 72,207 families, against Nokia's reported 20,000+. I sorted every family into one status using [this query](../sql/09_family_status.sql), and it processed about 15 MB.

| Status | Families | Share | Use in the model |
|---|---:|---:|---|
| **Granted, filed within 20 years** | **19,873** | 27.5% | **Core dataset** |
| **Recent application, may be pending** | **5,595** | 7.7% | Tracked separately |
| Granted, filed over 20 years ago | 22,649 | 31.4% | History only |
| No grant detected, older filing | 23,955 | 33.2% | History only |
| Names from sold businesses only | 135 | 0.2% | Excluded |
| **Total** | **72,207** | | |

**The workable portfolio is about 19,873 granted families, plus 5,595 possible pending ones.** The tables are `nokia_analytics.portfolio_30y` and `nokia_analytics.family_status`.

The core figure is close to Nokia's "over 20,000", which is encouraging. But it's not proof, as the errors below push in both directions and Nokia's counting rules aren't published.

## How the rules work

- **Granted:** not an international filing or a design, with a grant date or a kind code starting with B, C or E.
- **Within 20 years:** a granted document filed on or after 1 November 2006.
- **Possibly pending:** no grant detected, and filed since 1 January 2021.
- **Sold businesses:** every owner name matches cables, optronics, TCL or mobile, or submarine networks.

## Where the filter could be wrong

| Issue | Effect on 19,873 |
|---|---|
| Patents that lapsed because fees weren't paid | Too high |
| Patents sold to others, as old names remain | Too high |
| Grants missed outside the US, such as Japan | Too low |
| Pending applications older than 2021 | Not counted as pending |
| Grant dates that look wrong for some offices | Could go either way |

## US and Europe

| Office | Families with a detected grant in term | Share of 19,873 |
|---|---:|---:|
| United States | 15,468 | 78% |
| European Patent Office | 8,696 | 44% |
| China | 2,337 | 12% |

[Full list](../data/processed/in_term_by_office.csv). Families can appear in several offices. China and others are probably undercounted because of missing grant data.

The model will cover **both the US and Europe**. Nokia is a European company, and Europe matters as a market. US data is simply easier to start with, because one office records all renewals. In Europe, renewals move to national offices after grant, or to a Unitary Patent, so the data takes more work.

## Next checks

1. Spot-check a random sample against official registers.
2. Add USPTO renewal records to remove lapsed US patents.
3. Add USPTO assignment records to find US patents that were sold.
4. Find European legal status through Espacenet or a PATSTAT trial.
