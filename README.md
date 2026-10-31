# Patent Portfolio Analysis

**I'm doing this project to apply for Nokia's [Financial Data Engineering / Business Data Analytics Trainee — Patent Portfolio Management](https://www.linkedin.com/jobs/view/4483030441) traineeship, in the Business Data Analytics track.**

This isn't affiliated with Nokia, and it uses only public data.

## Central research question

> **How should Nokia prioritise its patent portfolio investments to support its AI and cloud infrastructure strategy?**
>
> Where is Nokia's patent portfolio strategically strong or exposed across optical networking, IP routing and data centre switching, how does its position compare with relevant competitors, and what do portfolio costs, technological developments and commercial trends suggest about future investment priorities?

~~How does Nokia's patent portfolio and associated investment position compare with the leading competitors in AI and cloud infrastructure networking, and what strategic and financial lessons can be identified?~~

I replaced the earlier question because it made comparing rivals the goal, while the role is about investment decisions. Comparisons and technology labels are now inputs to those decisions.

I didn't know what patent portfolio work involves, so this repo documents me teaching myself. After a couple of hours of exploring the data, testing questions and learning the field, I'd learned enough to zoom in on this question.

**How far public data can go:** it can show patent positions, technology trends and commercial signals, and it can estimate costs from official fees. It can't measure Nokia's real patent spending or investment efficiency, which would need internal data.

## Where it stands

| Research question | Output | Status |
|---|---|---|
| **1. What does Nokia own?** | Patent inventory by technology | 🟡 [Portfolio filtered](docs/portfolio-filter.md), [technology labels](docs/classification-codebook.md) not validated |
| **2. Where does it stand against competitors?** | Technology and competitor benchmark | 🟡 [Market leaders checked](docs/competitors.md), patent comparison is next |
| **3. Is the portfolio aligned with commercial growth?** | Technology-to-business assessment | 🟡 [Commercial and R&D signals](docs/competitors.md#investment-position) collected |
| **4. What do patent costs suggest about allocation?** | Public-data cost estimate and scenarios | 🟡 [US fees and a rough check](docs/strategy.md#early-answer-are-fees-big-enough-to-matter), needs USPTO records |
| **5. What should Nokia do differently?** | Scenarios and a recommendation | ❌ Not started |

**There's no answer to the main question yet.** The results below are the groundwork, and the patent comparison is still to come.

## What I've found so far

### No single company leads AI and cloud networking

Nokia's strongest public positions are in optical. Market share doesn't show who has the stronger patents, which is what I'm testing next.

![No single company leads AI and cloud networking](docs/img/ai_cloud_leaders.png)

### The workable portfolio is about 20,000 families

Nokia reports 26,000+ families, and my total including possibly pending ones is 25,468. Lapsed and sold patents are still included.

![From 72,207 families to a workable portfolio](docs/img/portfolio_filter.png)

### 46% of US patents filed since 1996 carry an Alcatel or Lucent name

That's across 36,630 unique patents, so any cost or renewal analysis needs to report them separately. These names show who's on each patent, not who owns it today or whether it's still in force.

![US patents by origin](docs/img/origin_30y.png)

### The patent data tracks Nokia's reported figures

New families follow Nokia's reported new inventions, and licensing sales swing with renewal cycles, from €1,085M in 2023 to €1,928M in 2024.

![Twenty years of Nokia's patents and money](docs/img/twenty_years.png)

### Renewal fees alone look small

A rough check puts official US renewal fees at about $14.5M–$18.8M a year, or roughly 1% of licensing-unit sales. Other offices and filing and attorney costs [aren't included yet](docs/strategy.md#early-answer-are-fees-big-enough-to-matter).

## How I work

- **Combining sources:** patent records, Nokia's annual reports, competitor and market data, and official fees
- **Verifying outputs:** cross-checks between sources, automatic checks and a record of what's still unverified
- **Using AI to move faster:** AI-accelerated search and analysis, with standard data handling and me directing the work
- **Building my own method:** a repeatable approach for my analytics and education
- **Learning quickly:** picking up new concepts and turning them into structured analysis
- **Directing my own research:** changing approach when something isn't working, and choosing where to spend my effort

## Guide to the repo

**The analysis**
- [What I have and still need](docs/evidence-gaps.md): evidence against each research question, and the order of work
- [Research design](docs/research-design.md): the five research questions, hypotheses and reliability rules
- [Analysis strategy](docs/strategy.md): the plan, and the financial analysis
- [Who leads AI and cloud networking?](docs/competitors.md): verified market positions and the comparison set
- [Technology codebook](docs/classification-codebook.md): how optical, IP routing and data centre switching are defined and tested
- [Twenty years of patents and money](docs/twenty-years.md): reported finances and events against the patent data
- [The workable portfolio](docs/portfolio-filter.md): how 72,207 families were narrowed

**Reliability**
- [Assumption register](docs/assumptions.md): what the analysis assumes, and what's been tested
- [Can I trust this data?](docs/data-trust.md): where it comes from, and where to find money data
- [Fact checks](docs/sources.md): the outside facts I rely on, and how well each one is supported
- [Working principles](docs/principles.md): the posting's expectations, how I apply them and where I fall short

**How I learned**
- [How I got here](docs/how-i-got-here.md): each step with screenshots, including mistakes
- [How my approach changed](docs/approach-changes.md): why I moved from exploring to testing hypotheses
- [Question log](docs/questions.md): how I found each answer and what I used
- [Data map](docs/data-map.md): what the data contains, and what's missing
- [Explain it yourself](docs/explain-it.md): the calculations and questions I should be able to answer

## Run it yourself

```bash
python src/clean_owners.py
python src/clean_lineage.py
python src/check_outputs.py
pip install matplotlib
python src/make_charts.py
python src/make_data_map.py
python src/make_scale_charts.py
python src/make_twenty_years_chart.py
python src/make_competitor_chart.py
python src/make_investment_chart.py
```

To get Nokia's annual reports, set your own contact, as the SEC requires one:

```bash
SEC_USER_AGENT="Your Name you@example.com" python src/download_annual_reports.py
```

The reports stay out of the repo because of their size, and [the manifest](data/raw/annual_reports_manifest.csv) records each file's source and fingerprint.

The queries are in [`sql/`](sql), numbered in the order I ran them. The working table expires after 60 days in the BigQuery sandbox, so rerun [the build query](sql/06_create_portfolio_30y.sql) to restore it.

## How this was made

I chose the question and data sources, ran the queries in BigQuery and reviewed the results. I used Claude (AI) to help interpret the output, write the scripts and draft this document.
