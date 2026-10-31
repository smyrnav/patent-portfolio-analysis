# Analysis strategy

I started by following whatever the data showed next. This page sets a method: start from a decision someone has to make, then work back to the data.

This is my outside view of what a portfolio team needs. Nokia's real priorities may differ, and the results are signals rather than proof.

## The central question

> Across the last 30 years, where is the portfolio strong, where is it exposed, and where might it be costing more than it should?

## What the data is made of

| Building block | Fields | Lets me compare by |
|---|---|---|
| **Inventions** | `family_id` | The basic unit of counting |
| **Filings** | `application_number`, `country_code` | How widely each invention is protected |
| **Time** | `priority_date`, `filing_date`, `grant_date` | Trends and expected expiry |
| **Technology** | `cpc_codes`, `title_en`, `abstract_en` | Which fields it covers |
| **Origin** | `owners` | Nokia, Alcatel, Lucent, Infinera and others |
| **People and places** | `inventors`, `inventor_countries` | Where the inventing happens |
| **Connections** | `cited_publications` | What each patent builds on |

## Answerable with my table now

| Business question | Decision it supports | Measure | Main limit |
|---|---|---|---|
| What does the portfolio cover? | Where to invest or prune | Inventions by technology and origin | Historical names, not confirmed current ownership |
| Where is momentum rising or falling? | Where to focus patent budgets | New inventions per period | The latest years are incomplete because of publication delays |
| When could protection run out? | When to refill a technology area | Filing date + 20 years, by technology | Latest possible date, as patents can lapse earlier |
| Where are the protection gaps? | Where to file | Share of inventions filed in each office, by technology | Filing is not the same as a granted patent |
| Which areas are costly to protect? | Where filing could be narrower | Offices per invention | Shows breadth, not actual money spent |
| What did each acquisition add? | How to value deals | Inventions by origin and technology | Names can be out of date |
| Where does inventing happen? | R&D site and key-person risk | Inventions by inventor country and inventor | 18% of publications lack inventor country |

## Needs more data

| Business question | What's missing |
|---|---|
| Which patents are still alive? | USPTO fee records or PATSTAT legal events |
| Which patents should be dropped? | Renewal history and a measure of value |
| What will the portfolio cost over 10 years? | Official fees for each office, plus assumptions |
| How does Nokia compare with rivals? | The same table for Ericsson, Huawei and others |
| Which patents matter for 5G? | ETSI declarations |
| Which patents have the most influence? | Who cites them, from another search of the full table |

## Can't be answered from public data

- Revenue or return per patent
- Licensing terms and who holds a licence
- Nokia's actual internal costs and its reasons for each decision

## The plan

1. **Clean the base:** review owner names, and settle the counting rules.
2. **Portfolio profile:** what it covers, by technology, period and origin.
3. **Momentum:** where new inventions are rising or falling.
4. **Expiry wall:** when protection could run out, by technology.
5. **Geographic gaps:** where each technology is protected.
6. **Add renewal data:** which patents owners actually keep, and what that costs.
7. **Decision brief:** one page on strengths, exposures and where to look for savings.

## Rule for each new question

Before running a query, I write down:

1. **The decision** it would inform
2. **The measure** I'd use
3. **What result would change my mind**
4. **The main limit** of the data

If I can't name the decision, it goes in a parking list instead of the plan.
