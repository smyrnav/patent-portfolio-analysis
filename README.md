# Patent Portfolio Analysis

A self-directed project, started after reading a job posting for a patent portfolio trainee at Nokia. I didn't know what that work involves, so I'm teaching myself by doing a version of it with public data.

This repo records each step: what I looked at, what I found and what I got wrong. It isn't affiliated with Nokia, and it uses only public data.

**Status:** Steps 1–5 are done. The cost model is not built yet.

## What I've found so far

| | |
|---|---|
| **187** | different owner names for what is mostly one corporate family |
| **94%** | of listings sit under just the top 10 names |
| **About 1 in 3** | listings come through Alcatel and Alcatel-Lucent, which Nokia acquired |
| **32% of names, 0.5% of listings** | the share of names that look like spelling or legal-form variants |
| **39** | listings that matched "Nokia" but belong to Nokian Tyres |

**Main takeaway:** the typos are easy to spot, but they barely change the totals. Knowing how the company is built, and which business lines it sold, matters far more.

## Step 1: Work out what the job actually is

The posting mentions patent costs, investment modelling, scenario analysis, and demand and capacity planning. My reading is that the team's core question is:

> Which patents are worth paying to keep, and how much should we spend?

Patents cost money to keep alive and earn money through licensing. The posting also spends a lot of time on data quality and on honest ranges rather than single numbers, so I decided to start with the data. This is my own inference from the posting, not something Nokia has told me.

## Step 2: Choose a data source

| | Google Patents Public Data | EPO PATSTAT Global |
|---|---|---|
| **Cost** | Free in the BigQuery sandbox, with 1 TB of queries a month | Paid |
| **Access** | Immediate, with SQL | Subscription, or a trial for PATSTAT Online |
| **Renewal data** | Not in the main table | Yes: `TLS231_INPADOC_LEGAL_EVENT`, `FEE_RENEWAL_YEAR`, `LAPSE_DATE` |
| **Owner names** | `assignee_harmonized` | `PSN_NAME`, `HAN_HARMONIZED` |

I chose Google so I could start straight away. I read the PATSTAT data catalog to see what the stronger source would add, and it's the natural upgrade for the European side.

## Step 3: Open the data

The main table is `patents-public-data.patents.publications`, with about 173.5 million rows and 2.88 TB. That size matters: the free allowance is 1 TB a month, so selecting only the columns I need is essential. `LIMIT` doesn't reduce what's scanned.

![The publications table in BigQuery](docs/img/01_publications_table.png)

## Step 4: Ask a simple question first

**Question:** under which names do Nokia's granted US patents appear?

[The query](sql/01_owner_names.sql) searches owner names containing "Nokia" or "Alcatel". I included Alcatel because Nokia bought Alcatel-Lucent in 2016.

![The first query and its results](docs/img/02_first_query.png)

I expected a short list and got 187 names ([raw results](data/raw/owner_counts.csv)).

## Step 5: Find out what the results mean

### The names reflect the company's history

Some of the largest names:

| Owner name | Granted US patents | What I think it is |
|---|---:|---|
| NOKIA CORP | 7,336 | Parent company |
| NOKIA TECHNOLOGIES OY | 6,431 | Technology and licensing company |
| ALCATEL LUCENT | 5,062 | Acquired in 2016 |
| NOKIA SOLUTIONS & NETWORKS OY | 2,401 | Networks business |
| CIT ALCATEL | 2,188 | Older Alcatel name |
| NOKIA MOBILE PHONES LTD | 977 | Former phone business |
| NOKIA SIEMENS NETWORKS OY | 531 | Former joint venture |

### Sorting them into families

[`src/clean_owners.py`](src/clean_owners.py) sorts every name into a family using simple rules, with the results in [`owner_mapping.csv`](data/processed/owner_mapping.csv).

![Listings by company family](docs/img/families.png)

### A few names hold almost everything

![Share of listings by owner name](docs/img/concentration.png)

### Three kinds of mess

1. **Typos:** `NOKIA TECHNOLGIES OY`, `Nokia Technololgies Oy`, `NOKIA MOVILE PHONES LTD`, `ALCATEL LUCENT USA ZINC`.
2. **Legal forms and subsidiaries:** `NOKIA OYJ`, `NOKIA INC`, `NOKIA GMBH`. These may be real, separate entities, so merging them is a decision about the question being asked.
3. **False matches:** `NOKIAN TYRES PLC` and `NOKIAN RENKAAT OYJ` are a tyre company. A simple text search catches them, and I only saw this by reading the output.

The script flags 59 names as likely variants, covering 140 listings. That's a floor, because the matching misses some, such as `NOKIA CORPORTION` against the much shorter `NOKIA CORP`, and some flagged names may be real entities.

A further 20 names (46 listings) are marked **Needs review**. They look like joint ownership or businesses that may have been sold, such as cables and optronics. I haven't verified their histories.

## What these numbers can't tell you

- **This isn't Nokia's current portfolio.** It includes expired patents and shows the name on the patent, which may be out of date after a sale or transfer.
- **Listings aren't unique patents.** A patent with two owners counts under both, so the 28,773 total is too high.
- **It's US-only.** A real portfolio spans many countries and patent families.
- **Family assignments are my judgement.** They need checking against company records.

## Next steps

1. Count unique patents, and keep only those likely to still be in force.
2. Add USPTO maintenance fee records to see which patents owners kept paying for.
3. Build a 10-year cost model using official fees, with simulated internal costs clearly labelled.
4. Show the result as a range, and test which assumptions matter most.
5. Write a one-page decision brief.

## Run it yourself

```bash
python src/clean_owners.py
pip install matplotlib && python src/make_charts.py
```

To refresh the raw data, run [the SQL](sql/01_owner_names.sql) in BigQuery and export it to `data/raw/owner_counts.csv`.

## How this was made

I chose the question and data sources, ran the queries in BigQuery and reviewed the results. I used Claude (AI) to help interpret the output, write the scripts and draft this document.
