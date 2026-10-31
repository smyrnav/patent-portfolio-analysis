# Twenty years of patents and money

I took the figures from Nokia's [20 annual reports](../data/raw/annual_reports_manifest.csv) and compared them with the patent data.

![Twenty years of Nokia's patents and money](img/twenty_years.png)

## The data

| File | Contents |
|---|---|
| [`nokia_financials_by_year.csv`](../data/processed/nokia_financials_by_year.csv) | Sales, R&D, licensing, reported families and inventions, FY2006–FY2025 |
| [`office_filings_by_year.csv`](../data/processed/office_filings_by_year.csv) | New families and US, European, Chinese and Japanese filings, 1996–2026 |
| [`nokia_events.csv`](../data/processed/nokia_events.csv) | 16 dated deals, disposals and licensing events, with source reports |

Financial figures are as first reported in each year's report, except where a note says otherwise. Each row names its source report, and later restatements are noted but not applied throughout.

## What I found

### My family counts follow Nokia's own numbers

| Year | New families in my data | Nokia's reported new inventions |
|---|---:|---:|
| 2018 | 1,270 | more than 1,300 |
| 2019 | 1,233 | more than 1,300 |
| 2020 | 1,363 | more than 1,500 |
| 2021 | 1,626 | more than 1,500 |
| 2022 | 1,618 | more than 1,700 |
| 2023 | 1,966 (provisional) | more than 2,300 |
| 2024 | 2,471 (provisional) | more than 3,000 |

This is the strongest check so far that family counts are measuring something real. Both are rising, and the recent gap is what publication delay would produce.

### Portfolio size has two reported levels

Nokia reported more than 26,000 families in FY2016, around 20,000 from FY2017 to FY2023, and 26,000+ in FY2025. My filter gives 19,873 granted families, plus 5,595 possibly pending, or 25,468 in total. That total is close to 26,000, but Nokia doesn't publish its counting rules, so this doesn't prove the two match.

**Unexplained:** I haven't found why the figure fell by about 6,000 between FY2016 and FY2017, or why it rose again by FY2025. Infinera wouldn't account for all of the rise, so this stays open.

### Licensing income moves with renewal cycles

Licensing-unit sales fell to €1,085M in 2023, then rose to €1,928M in 2024 as the smartphone renewal cycle ended, and the report puts the contracted run-rate at about €1.4B in 2025. A yearly value per family would swing with these deals, so a budget model shouldn't rely on one year.

### Japan needed fixing

Searching by owner name found only 831 of 4,376 Japanese filings since 2010, or 19%, as many Japanese records have no owner name. Finding filings by family recovers the rest. Families filed only in Japan would still be missed, and grant counts for Japan remain unreliable.

### China is rising, with a caveat

China passes the US in 2024 with 1,363 filings against 1,137. Recent years are incomplete and publication timing can differ by office, so this needs rechecking later.

## What this can't show

- **Cause and effect:** 20 yearly points show patterns, and group changes in 2013 and 2016 break the series.
- **Typical patent costs:** I found no patent cost figures in a targeted search of these reports. Mean and median costs need fee schedules and renewal records instead.
