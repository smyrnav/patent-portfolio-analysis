# Analysis strategy

I started by following whatever the data showed next. This page sets a method: start from a decision someone has to make, then work back to the data. [Here's why I changed approach](approach-changes.md).

This is my outside view. Nokia's real priorities may differ, and patent data gives signals to investigate rather than final answers.

![Five business questions, and what each one needs](img/question_map.png)

## The five questions

| Question | What I can show | What I can't show |
|---|---|---|
| **Portfolio efficiency:** which patents are worth maintaining, developing or reconsidering? | A shortlist based on renewal history, remaining life, breadth, citations and overlap | The final decision, which needs legal review and internal licensing value |
| **Competitive intelligence:** where are competitors gaining technological advantages? | Growth and share by technology and market, against rivals | Whether more patents means better technology or products |
| **Technology strategy:** where should Nokia invest in R&D? | Where the portfolio is thinning, and where rivals are moving | Whether the investment would pay off, which needs market and cost data |
| **Commercial intelligence:** which parts of the portfolio have licensing potential? | Candidates with declared standards links, outside citations and life left | Actual licensing value, terms or licensees |
| **Market foresight:** which emerging technologies could become commercially important? | Fast growth from a small base, new entrants and standards activity | Commercial demand, and the latest inventions because of publication delay |

## What each question needs

![Which data each question needs](img/question_data_matrix.png)

## Order of work

1. **Portfolio efficiency.** It's closest to the job posting, and renewal records can be used without scanning the big BigQuery table.
2. **Competitive intelligence.** A rival table also feeds the next question.
3. **Technology strategy.** It combines my portfolio view with the rival view.
4. **Commercial intelligence.** It adds ETSI declarations and the patents citing Nokia's.
5. **Market foresight.** It needs the widest data, so it comes last.

Each one ends in a short brief covering the finding, the evidence, the limits and the decision it supports.

## How the earlier questions fit

They're now measures inside the five questions:

| Earlier question | Now part of |
|---|---|
| Protection cliff, Costly coverage | Portfolio efficiency |
| Geographic gaps | Competitive intelligence, once compared with rivals |
| Refill rate, Dependency | Technology strategy |
| Deal value | Portfolio efficiency and Commercial intelligence |
| Keep or drop, 10-year budget | Portfolio efficiency |
| Rival benchmark | Competitive intelligence |
| Standards exposure | Commercial intelligence and Market foresight |

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

## Rule for each new question

Before running a query, I write down:

1. **Which of the five questions** it serves
2. **The decision** it would inform
3. **The measure** I'd use
4. **What result would change my mind**
5. **The main limit** of the data

If it doesn't serve one of the five, or the answer is already obvious, the query doesn't get run.
