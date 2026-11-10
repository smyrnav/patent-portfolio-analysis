# Satcom hypotheses

**Status: draft, 8 November 2026.** Re-aims the [retired H1–H4](research-questions.md#hypotheses) at the sovereign satcom question, as the [pivot checklist](pivot-sovereign-satcom.md#checklist-to-execute-the-pivot) planned ("new hypotheses drafted after the code pools exist"). The pools are the five candidates in [satcom-code-pools.md](satcom-code-pools.md), and every test below is gated by the [validation plan](../02-methodology/satcom-validation-plan.md). Nothing here has been run.

## The three hypotheses

| # | Hypothesis | Feeds | Test | What would disprove it |
|---|---|---|---|---|
| **H1** | The distribution of patent families across the five capability pools (SAT, ISL, GRD, NET, SEC) differs between the actors in scope (Nokia, ICEYE, Eutelsat/OneWeb, Viasat, Thales Alenia Space, Airbus Defence and Space) | RQ1, RQ2 | [Chi-square test of independence, with Cramér's V](../glossary.md#statistics-in-plain-language) | The distributions are statistically indistinguishable, or the effect size is near zero |
| **H2** | The share of each actor's new families falling in the satcom pools has risen across priority cohorts, and the trend differs by actor | RQ3 | [Cochran–Armitage trend test](../glossary.md#statistics-in-plain-language) per actor, or [logistic regression](../glossary.md#statistics-in-plain-language) of in-pool membership on cohort, with an actor interaction | The trends are flat, or identical across actors |
| **H3** | Within the same pool, forward-citation patterns differ between actors | RQ3 | [Kruskal–Wallis](../glossary.md#statistics-in-plain-language), or a regression controlling for filing cohort and office | No difference once age and office are controlled |

Statistical terms used below ([chi-square, p-value, effect size, degrees of freedom, residuals](../glossary.md#statistics-in-plain-language)) are defined in the glossary in plain language.

H3 needs the age control to be fair: citations accumulate over time, so a raw comparison would punish young portfolios like ICEYE's for being young, not for being weak.

## The main test, specified in advance (H1)

H1 is the strongest candidate: it maps directly onto "who has what, and what does ICEYE add."

- **Question:** is portfolio composition across the five pools associated with the actor?
- **H₀:** actor and pool distribution are independent. **H₁:** the distribution differs by actor.
- **Unit:** the simple patent family — one invention, one row. National filings of the same invention must not be counted twice.
- **Test:** chi-square test of independence, significance threshold 0.05.
- **Effect size:** Cramér's V.
- **Report:** observed counts, expected counts, proportions, the test statistic, degrees of freedom, the p-value, and V — plus **standardized residuals**, which show which actor×pool cells drive the result. For the central question, the cells that matter are Nokia×NET (integration is Nokia's claimed strength), ICEYE×SAT (does the partner bring space-segment patents or not), and anyone×SEC.

### Assumption checks, decided before seeing data

| Check | Rule |
|---|---|
| Expected cell counts | At least 5 per cell. If a pool is too rare (the census may show ISL is tiny), that pool leaves the test and the exclusion is reported — cells are not quietly merged |
| Time bias | Restrict to the 2020–2024 main comparison period; 2025–2026 are provisional because publication lags filing by about 18 months |
| Coverage | State which offices the count covers; US-heavy coverage is a known limit, not a footnote |
| Independence | Family-level counting handles the related-filings problem; families sharing a priority are the same unit by construction |

## What data the tests may use

This rule protects the whole exercise, because the pre-pivot pools [failed the 85% precision bar](../02-methodology/validation.md#precision-result) — raw code counts flattered Nokia over its competitors.

| Tier | Data | What it's allowed to support |
|---|---|---|
| 1 | Raw code-pool counts | Description only. **Never** a significance test |
| 2 | Precision-adjusted estimates (counts corrected by measured per-pool, per-company precision) | H1–H3, with ranges, once validation stage 3 passes |
| 3 | Hand-labelled sample | H1–H3 on the labelled set, small n and wide intervals, once stage 4 passes |

If a pool fails validation, H1 either drops that pool or runs as descriptive statistics, labelled as such. A significant result computed on invalid data would be worse than no result.

## What a significant result would and wouldn't mean

A significant chi-square shows an **association** between actor and portfolio composition. It would not show that one portfolio is better, and it would not show that anyone's investment strategy caused the difference — public patent data can't reveal internal decisions. The hypotheses connect the data to the strategic question without pretending otherwise.

## Sequence

Pool census (validation stage 0) → pilot → freeze → precision → H1 runs on tier-2 data; H2 needs the period-stratified counts from the same work; H3 needs the citation fields already sitting unanalysed in the BigQuery table. Tier-3 runs after human labelling, per the [validation plan](../02-methodology/satcom-validation-plan.md#the-human-labelling-problem-stated-plainly).
