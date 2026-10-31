# How my approach changed

A record of how this project's method changed, and why.

## The turning point

I got annoyed with running random queries. Each result suggested another question, and I kept following them without knowing what any of it was for. When "did Nokia move from phones to networks?" came up, I realised the answer was obvious and nobody would decide anything differently because of it, so I stopped and rethought the approach.

## Before and after

| | Before | After |
|---|---|---|
| **Starting point** | Whatever the last result showed | A decision someone has to make |
| **Main question** | What's in this data? | How should a limited patent budget be allocated? |
| **Choosing a query** | It seemed interesting | It has to inform a named decision |
| **Unit of analysis** | Mostly owner names and listings | Inventions (patent families) |
| **Data source** | The 2.88 TB table each time | My own 30-year working table |
| **Result** | A trail of facts | A budget allocation model and a decision brief |

## What changed along the way

1. **Started with exploration.** I wanted to learn what this work involves, so I began with the question "under which names do Nokia's patents appear?". That taught me how messy the data is, and it was useful as a way to get oriented.
2. **Checked my numbers against each other.** Comparing two totals exposed that my kind code filter had dropped 8,808 older US patents, so I now cross-check totals before trusting them.
3. **Narrowed the scope to 30 years.** That covers everything that could still be alive, plus 10 years of history.
4. **Isolated the data.** Building one working table means later questions don't have to rescan the source table. It used about 289 GB once.
5. **Paused to set a strategy.** I listed what the data can and can't answer, then rebuilt the questions around decisions.
6. **Dropped a query.** I deleted the technology-over-time query before running it, because it only confirmed the obvious on its own.
7. **Raised the questions to business level.** My first list was mostly measures, like when patents expire. I replaced it with five questions a company would actually ask: technology strategy, competitive intelligence, commercial intelligence, portfolio efficiency and market foresight. The earlier measures now sit inside them.
8. **Focused on the role.** The posting has a track for turning patent and financial data into investment decisions, so the project now centres on allocating a limited patent budget. Its outputs are a cost forecast, keep-or-drop analysis, scenarios, sensitivities, a capacity plan and a decision brief. Competitive and licensing questions are parked for now.

## The rule I use now

Before running a query, I write down:

1. **Which deliverable** it feeds
2. **The decision** it would inform
3. **The measure** I'd use
4. **What result would change my mind**
5. **The main limit** of the data

If it doesn't feed a deliverable, the query doesn't get run.

## What I kept from the exploration

The exploration wasn't wasted. It's how I found the messy names, the deal history in the data, the kind code gap and the fields that are too incomplete to rely on. Those findings now shape the strategy.

See the [analysis strategy](strategy.md) for the current plan.
