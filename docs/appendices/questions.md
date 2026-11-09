# Question log

These are the questions from my exploration, kept as a research notebook. The [research questions](../01-research-design/research-questions.md) I'm now working towards are separate.

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

### Q26. Which connectivity needs can Direct-to-Cell services cover, and which need a dedicated sovereign system?
- **Why I asked:** Kyivstar's Starlink Direct-to-Cell service reached millions of users, so it's tempting to read that as proof of demand for a sovereign broadband constellation — but it's a different product (messaging and light data to ordinary phones, not dedicated broadband).
- **Why it matters:** RQ3 and RQ4 need to know which requirements existing services already satisfy, or the build–buy–partner–license matrix compares the wrong things.
- **How I'll look:** desk research comparing Direct-to-Cell, conventional Starlink, OneWeb and the proposed Nokia–ICEYE system against each requirement. Verified starting points: [Kyivstar's 3-million announcement](https://investors.kyivstar.ua/news-releases/news-release-details/kyivstar-reaches-3-million-customers-starlink-direct-cell-and) and [Light Reading, 10 September 2026](https://www.lightreading.com/satellite/lessons-from-a-war-zone-how-ukraine-s-kyivstar-harnesses-starlink-to-keep-users-online) (7.5M connected, 10M+ SMS, SMS/light-data scope).

### Q25. Does ICEYE hold satellite-communications patents at all?
- **Why I asked:** ICEYE's heritage is radar imaging (SAR), so its patent record may be radar-heavy and comms-thin — and "what ICEYE adds" (RQ1) can't be answered by press releases alone.
- **Why it matters:** if the record is thin, that's a finding about the partnership's division of labour, not a data error.
- **How I'll look:** ICEYE name research, then the pool census in BigQuery against the five satcom pools.
- **Tools and resources:** BigQuery, [satcom code pools](../01-research-design/satcom-code-pools.md).

### Q24. Under which names do the new satcom actors file patents?
- **Why I asked:** the new comparison set is made of joint ventures, divisions and mergers — Thales Alenia Space (Thales/Leonardo), Airbus Defence and Space (a division), OneWeb (merged into Eutelsat, filed as WorldVu Satellites), Viasat (bought Inmarsat). Get the names wrong and every later count is wrong in a direction nobody can see.
- **How I'll look:** the same procedure as Q5 and Q6 — applicant-name queries per company, read the variants, document the mapping before building any table.
- **Tools and resources:** BigQuery applicant-name queries, then `data/interim/` for the mapping.

### Q23. Which patent classification codes find satellite communications patents?
- **Why I asked:** the pivot needed satcom code pools defined from the classification schedules, not guessed.
- **How I looked:** read the USPTO CPC scheme pages for H04B, H04W and H04K directly.
- **Answer:** five candidate pools (SAT, ISL, GRD, NET, SEC), documented with sources in [satcom-code-pools.md](../01-research-design/satcom-code-pools.md). Candidates only — each pool still has to pass the precision bar before any comparison, per the [validation plan](../02-methodology/satcom-validation-plan.md).
- **What it led to:** Q24 and Q25.

### Q22. How much of the portfolio I attribute to Nokia does it still own?
- **Why I asked:** while checking applicant/assignee names in my codebook sample, 42 of the 179 unique Nokia-lineage patents (23.5%) showed a current assignee on Google Patents outside Nokia, Alcatel, Lucent and Infinera. This isn't verified legal ownership. They include WSOU Investments 23, RPX 15, and 4 others. Recorded assignments on the pages I opened show transfers, such as [US8432894B2](https://patents.google.com/patent/US8432894B2/en) to WSOU and [US9825759B2](https://patents.google.com/patent/US9825759B2/en) to Provenance and then RPX.
- **Why it matters:** my tables use `assignee_harmonized`, which keeps the name from filing, so my 19,873 families with grant evidence can include patents held by others. The other four companies show this far less: 2 of 242. Nokia's reported 26,000+ may therefore match my 25,468 partly by coincidence.
- **How I'll look:** estimate the share with a random US sample across the portfolio, as this sample covers only three technologies. Then check it against USPTO assignment records. It could also help explain Q20.
- **Tools and resources:** Google Patents legal events, and USPTO assignment data.

### Q21. Has someone already labelled these patents, so I don't need to?
- **Why I asked:** labelling hundreds of patents by hand seemed like work someone must have done.
- **How I looked:** searched for labelled datasets and landscape reports, then read the two most relevant.
- **Answer:** I found nothing that fits. [CinPatent](https://arxiv.org/abs/2212.12192v3) has 45,131 English patents, but its labels are CPC codes, so testing codes with it would be circular. [Patsnap's optical landscape](https://www.patsnap.com/resources/blog/rd-blog/optical-networking-patent-landscape-patent-landscape/) has no downloadable list I could find and doesn't publish its search. Its top ten includes ServiceNow, Bright Data and KnowBe4, so it isn't a clean optical benchmark. [Knowmade's report](https://www.knowmade.com/wp-content/uploads/2026/01/CPO-and-Optical-Interconnects-Patent-Landscape-2026-SAMPLE.pdf) is paid and covers one niche. Two searches can't prove nothing exists. The existing work I could reuse is the examiners' codes, and [my test](../02-methodology/validation.md#precision-result) shows how far they can be trusted: 73% for optical, 39% for routing, 42% for H04L 49 switching.
- **Tools and resources:** web search, Google Patents and BigQuery.
- **What it led to:** Q22.

### Q20. Why did Nokia's reported portfolio fall from 26,000+ to about 20,000, then return to 26,000+?
- **Why I asked:** it's a change of about 6,000 families, and my searches of the reports haven't explained it.
- **How I'll look:** read the FY2016, FY2017 and FY2025 reports closely, then look for lapses or sales in USPTO records.

### Q13. Did Lucent's patents actually stay in the family?
- **Why I asked:** Lucent spun off Avaya and Agere ([fact checks](sources.md)), so a Lucent name may not lead to Nokia today.
- **How I'll look:** patent assignment records for a sample of Lucent patents, and company histories.

### Q7. How many unique Nokia patents are still alive?
- **Why I asked:** my totals count co-owned patents twice and include expired ones.
- **How I'll look:** count distinct publication numbers across the cleaned names, then filter by grant date and renewal status.

### Q8. Which patents do owners stop paying for, and when?
- **Why I asked:** this is the closest public evidence for the keep-or-drop decision.
- **How I'll look:** USPTO maintenance fee records, with fees due at 3.5, 7.5 and 11.5 years.

### Q9. What would keeping a portfolio cost over 10 years, as a range?
- **Why I asked:** the posting asks for ranges and tested assumptions rather than one number.
- **How I'll look:** the [ten-year maintenance cost model](../04-financial-analysis/ten-year-maintenance-cost-model.md): official fees on verified national rights, with scenarios, and Monte Carlo only where distributions can be justified. Internal costs stay out of the baseline.

## Answered

### Q19. How do Nokia's reported finances line up with its patent activity?
- **Why I asked:** patent data has no money in it, and the annual reports are the main public source of it.
- **How I looked:** [extracted figures from 20 reports](../03-market-and-patent-analysis/twenty-years.md), and compared them with new families per year.
- **Answer:** new families follow Nokia's reported new inventions closely, and reported licensing income varied around the smartphone renewal cycle. Nokia's reports attribute the 2024 rise to renewal timing; this is an observed pattern, not tested causation.
- **Tools and resources:** SEC EDGAR, Nokia's 20-F reports and BigQuery.
- **What it led to:** Q20 and the Japan fix.

### Q18. How do I narrow 72,207 families to something I can work with?
- **Why I asked:** a cost forecast on the raw table would be far too high, as Nokia reports just over 20,000 families.
- **How I looked:** [sorted every family by status](../../sql/09_family_status.sql).
- **Answer:** 19,873 families with grant evidence within 20 years, plus 5,595 families with a recent application and no grant detected. Absence of a detected grant isn't proof that an application is pending. Lapsed and transferred patents are still in there. See [the candidate universe](../02-methodology/candidate-portfolio-universe.md).
- **Tools and resources:** BigQuery and my working table.
- **What it led to:** spot-checks, plus USPTO renewal and assignment records.

### Q17. What are the corrected US numbers?
- **Why I asked:** my early counts missed older patents, so I couldn't rely on them.
- **How I looked:** [recounted from the working table](../../sql/08_recount_us_30y.sql) ([results](../../data/processed/us_30y_recount.csv)), which processed 14.46 MB.
- **Answer:** 36,630 distinct US publications under 238 applicant/assignee names and 37,710 owner-publication listings. Origin counts overlap and sum to 36,866, so a distinct Alcatel/Lucent share awaits a corrected publication-level SQL rerun. The top 10 names account for 93% of listings, not unique patents or current ownership.
- **Tools and resources:** BigQuery and my working table.
- **What it led to:** the current figures in the README.

### Q10. Which of the "Needs review" names did Nokia actually inherit?
- **Why I asked:** some names look like joint ownership or businesses that may have been sold.
- **How I looked:** checked company histories online, and recorded them in my [fact checks](sources.md#the-needs-review-names).
- **Answer:** several look like businesses that left, such as cables, optronics and the TCL mobile venture. They cover only 178 patents, about 0.5%, so they barely affect the picture. A few remain unknown, and patent-level records would be needed to prove ownership.
- **Tools and resources:** encyclopedia and trade sources.
- **What it led to:** no change to the plan, as the effect is small.

### Q15. What does the portfolio look like over the last 30 years?
- **Why I asked:** the all-years rerun showed Lucent's biggest name almost doubling to 9,310 patents ([top 20 names](../../data/raw/owner_counts_all_years_top20.csv)). It also pulled in old businesses and false matches, including a person called Craig Enokian. The last 30 years cover everything that could still be alive, plus 10 years of history.
- **How I looked:** [built a working table](../../sql/06_create_portfolio_30y.sql), then [checked it](../../sql/07_check_portfolio_30y.sql) ([results](../../data/raw/portfolio_30y_check.csv)).
- **Answer:** 289,998 publications from 212,660 applications and 72,207 patent families, across 64 offices. That's about 2.9 applications per invention. Citations are missing on 49% of publications, English abstracts on 21%, inventor countries on 18%, English titles on 13%, and technology codes on 2%.
- **Tools and resources:** BigQuery.
- **What it led to:** the [research design](../01-research-design/research-design.md). Later queries can use this table instead of the 2.88 TB source.

### Q14. Did my first two searches miss older US patents?
- **Why I asked:** the country query found 43,674 granted US applications, more than the 34,229 listings from my earlier searches, even though those double-count some patents.
- **How I looked:** [counted US patents by kind code](../../sql/04_check_us_kind_codes.sql) ([results](../../data/raw/us_kind_codes.csv)).
- **Answer:** yes. Filtering on B dropped 8,808 A patents, the last granted in December 2000, plus 1,609 design patents and 123 reissues. So the totals and shares from Q5, Q6 and Q11 are too low or incomplete.
- **Tools and resources:** BigQuery, and comparing totals from two different queries.
- **What it led to:** Q15. Design patents protect how a product looks, so they need separate treatment in any technology analysis.

### Q12. Where does Nokia file, including China and Europe?
- **Why I asked:** I started with the US because it's easier, not because I knew it mattered most.
- **How I looked:** [counted applications and patent families by office](../../sql/03_filings_by_country.sql).
- **Answer:** US 56,039, European Patent Office 44,353, China 24,662, and Germany 13,141. The US is the largest, but Europe is close, and 79% of the US total.
- **Tools and resources:** BigQuery. EP is the European Patent Office rather than the EU, and WO filings aren't patents yet.
- **What it led to:** Q14, and a warning that grant dates can't be compared across countries. Japan shows 0 granted, while Austria shows 99.8%.

### Q11. Which companies' patents did the portfolio come from?
- **Why I asked:** the first search only covered names with "Nokia" or "Alcatel", and I realised Alcatel had merged with Lucent.
- **How I looked:** listed the deals I knew of, then [searched for the missing names](../../sql/02_lineage_names.sql).
- **Answer:** Lucent and Infinera were both missing from my first search. The early listing-based comparison was superseded by Q17: overlapping origin counts cannot establish a distinct Alcatel/Lucent share. This shows where listings came from, not what Nokia owns today.
- **Tools and resources:** BigQuery, whole-word regular expressions, and the deal history, later checked in my [fact checks](sources.md).
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
- **Why I asked:** I needed a way to reach the data.
- **How I looked:** followed the sandbox setup and opened the table.
- **Answer:** the data stays on Google's side, and you query it with SQL. The sandbox needs no card, and the Schema and Preview tabs are free. The table is 2.88 TB, so choose columns carefully, as `LIMIT` doesn't reduce what's scanned.
- **Tools and resources:** [BigQuery sandbox docs](https://docs.cloud.google.com/bigquery/docs/sandbox).
- **What it led to:** Q5.

### Q5. Under which names do Nokia's US patents appear?
- **Why I asked:** I needed to find the portfolio before analysing it.
- **How I looked:** ran [a query](../../sql/01_owner_names.sql) on owner names containing "Nokia" or "Alcatel".
- **Answer:** 187 names in my first search, later corrected to 238 in Q17.
- **Tools and resources:** BigQuery and the `assignee_harmonized` field.
- **What it led to:** Q6.

### Q6. What do those 187 names mean?
- **Why I asked:** I couldn't count anything until I knew which names were really the same company.
- **How I looked:** read the output, then wrote [rules to group the names](../../src/clean_owners.py).
- **Answer:** they reflect the company's history, plus typos and false matches. Nokian Tyres matched only because of its name. The likely typos make up 32% of names but only 0.5% of listings, so they barely change the totals.
- **Tools and resources:** Python and `difflib`.
- **What it led to:** Q7 and Q10.
