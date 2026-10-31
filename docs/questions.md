# Question log

These are the questions from my exploration. The business questions I'm now working towards are in the [analysis strategy](strategy.md).

Every question I ask while teaching myself this work, how I went about answering it, and what I used. New questions go at the top of "Open".

To add one, copy this:

```markdown
### Q0. The question
- **Why I asked:**
- **How I looked:**
- **Answer:**
- **Tools and resources:**
- **What it led to:**
```

## Open

### Q13. Did Lucent's patents actually stay in the family?
- **Why I asked:** as far as I remember, Lucent spun off Avaya and Agere, so a Lucent name may not lead to Nokia today.
- **How I'll look:** patent assignment records for a sample of Lucent patents, and company histories.

### Q7. How many unique Nokia patents are still alive?
- **Why I asked:** the 28,773 total counts co-owned patents twice and includes expired ones.
- **How I'll look:** count distinct publication numbers across the cleaned names, then filter by grant date and renewal status.

### Q8. Which patents do owners stop paying for, and when?
- **Why I asked:** this is the closest public signal for the keep-or-drop decision.
- **How I'll look:** USPTO maintenance fee records, with fees due at 3.5, 7.5 and 11.5 years.

### Q9. What would keeping a portfolio cost over 10 years, as a range?
- **Why I asked:** the posting asks for ranges and tested assumptions rather than one number.
- **How I'll look:** official fee schedules, simulated internal costs labelled as simulated, and a Monte Carlo model.

### Q10. Which of the "Needs review" names did Nokia actually inherit?
- **Why I asked:** 20 names look like joint ownership or businesses that may have been sold.
- **How I'll look:** company histories and patent assignment records.

## Answered

### Q15. What does the portfolio look like over the last 30 years?
- **Why I asked:** the all-years rerun showed Lucent's biggest name almost doubling to 9,310 patents. It also pulled in old businesses and false matches, including a person called Craig Enokian. The last 30 years cover everything that could still be alive, plus 10 years of history.
- **How I looked:** [built a working table](../sql/06_create_portfolio_30y.sql), then [checked it](../sql/07_check_portfolio_30y.sql) ([results](../data/raw/portfolio_30y_check.csv)).
- **Answer:** 289,998 publications from 212,660 applications and 72,207 patent families, across 64 offices. That's about 2.9 applications per invention. Citations are missing on 49% of publications, English abstracts on 21%, inventor countries on 18%, English titles on 13%, and technology codes on 2%.
- **Tools and resources:** BigQuery. Still to review: the owner names in the table, since some false matches or sold businesses may remain.
- **What it led to:** the [analysis strategy](strategy.md). Later queries can use this table instead of the 2.88 TB source.

### Q14. Did my first two searches miss older US patents?
- **Why I asked:** the country query found 43,674 granted US applications, more than the 34,229 listings from my earlier searches, even though those double-count some patents.
- **How I looked:** [counted US patents by kind code](../sql/04_check_us_kind_codes.sql) ([results](../data/raw/us_kind_codes.csv)).
- **Answer:** yes. Filtering on B dropped 8,808 A patents, the last granted in December 2000, plus 1,609 design patents and 123 reissues. So the totals and shares from Q5, Q6 and Q11 are too low or incomplete.
- **Tools and resources:** BigQuery, and comparing totals from two different queries.
- **What it led to:** Q15. Design patents protect how a product looks, so they need separate treatment in any technology analysis.

### Q12. Where does Nokia file, including China and Europe?
- **Why I asked:** I started with the US because it's easier, not because I knew it mattered most.
- **How I looked:** [counted applications and patent families by office](../sql/03_filings_by_country.sql).
- **Answer:** US 56,039, European Patent Office 44,353, China 24,662, and Germany 13,141. The US is the largest, but Europe is close, so starting with the US was reasonable but tells only part of the story.
- **Tools and resources:** BigQuery. EP is the European Patent Office rather than the EU, and WO filings aren't patents yet.
- **What it led to:** Q14, and a warning that grant dates can't be compared across countries. Japan shows 0 granted, while Austria shows 99.8%.

### Q11. Which companies' patents did the portfolio come from?
- **Why I asked:** the first search only covered names with "Nokia" or "Alcatel", and I realised Alcatel had merged with Lucent.
- **How I looked:** listed the deals I knew of, then [searched for the missing names](../sql/02_lineage_names.sql).
- **Answer:** Lucent adds 4,772 listings and Infinera 705, so about 4 in 10 listings trace back to Alcatel-Lucent. This shows where listings came from, not what Nokia owns today.
- **Tools and resources:** BigQuery, whole-word regular expressions, and my memory of the deal history, still to be checked.
- **What it led to:** Q12 and Q13. It also found 10 misspelled Alcatel names that the first search missed, and 7 unrelated companies, such as Lucent Medical Systems, that a text search can't rule out.

### Q1. What does a patent portfolio team actually do?
- **Why I asked:** the posting caught my eye, but I didn't know what the work is.
- **How I looked:** read the posting closely and pulled out the repeated themes.
- **Answer:** my reading is that they decide which patents are worth keeping and how much to spend, and that messy data is a large part of the work. This is inference, not confirmed by Nokia.
- **Tools and resources:** the job posting.
- **What it led to:** Q2.

### Q2. Where can I get patent data without working there?
- **Why I asked:** I needed real data to practise on.
- **How I looked:** compared Google's public datasets with EPO PATSTAT on cost, access and contents.
- **Answer:** Google for now because it's free and immediate, with PATSTAT as the upgrade for renewal and lapse data.
- **Tools and resources:** [Google Patents Public Datasets](https://cloud.google.com/blog/topics/public-datasets/google-patents-public-datasets-connecting-public-paid-and-private-patent-data), [PATSTAT](https://www.epo.org/en/about-us/observatory-patents-and-technology/observatory-tools/patstat), [PATSTAT Online pricing](https://shop.epo.org/en/Data-and-services/Online-services/PATSTAT-Online/p/PAI-online).
- **What it led to:** Q3 and Q4.

### Q3. What is a "data catalog"?
- **Why I asked:** I saved the PATSTAT catalog and didn't know what it was.
- **How I looked:** read through its tables and fields.
- **Answer:** it's the manual for the database, listing every table and column, and it contains no patents itself. It showed that PATSTAT records renewal years and lapse dates.
- **Tools and resources:** PATSTAT Global data catalog, autumn 2026 edition.
- **What it led to:** a clear idea of what the free data is missing.

### Q4. How do I get into the Google data?
- **Why I asked:** I'd never used BigQuery.
- **How I looked:** followed the sandbox setup and opened the table.
- **Answer:** the data stays on Google's side, and you query it with SQL. The sandbox needs no card, and the Schema and Preview tabs are free. The table is 2.88 TB, so choose columns carefully, as `LIMIT` doesn't reduce what's scanned.
- **Tools and resources:** [BigQuery sandbox docs](https://docs.cloud.google.com/bigquery/docs/sandbox).
- **What it led to:** Q5.

### Q5. Under which names do Nokia's US patents appear?
- **Why I asked:** I needed to find the portfolio before analysing it.
- **How I looked:** ran [a query](../sql/01_owner_names.sql) on owner names containing "Nokia" or "Alcatel".
- **Answer:** 187 names, with the top 10 holding 94% of listings.
- **Tools and resources:** BigQuery and the `assignee_harmonized` field.
- **What it led to:** Q6.

### Q6. What do those 187 names mean?
- **Why I asked:** I couldn't count anything until I knew which names were really the same company.
- **How I looked:** read the output, then wrote [rules to group the names](../src/clean_owners.py).
- **Answer:** they reflect the company's history, plus typos and false matches. Nokian Tyres matched only because of its name. The typos make up 32% of names but only 0.5% of listings, so company structure matters more.
- **Tools and resources:** Python and `difflib`.
- **What it led to:** Q7 and Q10.
