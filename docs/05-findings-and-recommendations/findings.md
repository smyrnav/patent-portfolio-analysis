# Findings so far

**There's no answer to the central question yet.** These are provisional findings, in the [required format](../01-research-design/research-design.md#how-to-state-an-answer). The executive brief gets written once RQ5 has evidence behind it.

## 1. Patent codes can't be used alone to compare companies

- **Evidence:** claims earned the matching class in [73 of 100 optical, 39 of 100 routing and 42 of 100 H04L 49 patents](../02-methodology/validation.md#precision-result), against my 85% bar. Precision also [falls in newer patents](../02-methodology/validation.md#precision-by-priority-period).
- **Confidence:** medium. The gaps are large, but the labels are a software-generated first pass; human review and human–software agreement aren't done.
- **What would change it:** independent human hand-labels disagreeing with the first pass, or a looser rule on control-plane claims.
- **Decision:** use claim-based estimates with ranges, and stop using raw code counts.

## 2. A large share of Nokia-lineage patents may be held by others, unlike the other four companies

- **Evidence:** [42 of 179 sampled patents (23.5%)](../02-methodology/candidate-portfolio-universe.md#current-owner-evidence-so-far) show another current assignee on Google Patents, against 2 of 242 for the others.
- **Confidence:** medium for the direction, low for the size. Google Patents isn't a register, and the sample covers three technologies.
- **What would change it:** USPTO assignment records on a random US sample showing a much lower share.
- **Decision:** investigate before any cost or comparison work uses applicant counts. Report Nokia with and without these patents.

## 3. Nokia's lineage looks strongest in optical and thinnest in switching

- **Evidence:** [estimated US families](../03-market-and-patent-analysis/patent-landscape.md#estimated-us-families-by-company) of 768 optical, 233 routing and 70 switching. Cisco has an estimated 792 in routing and 220 in switching.
- **Confidence:** low. Samples are small, recall isn't tested, and the figures cover all years rather than 2020–2024.
- **What would change it:** recall results, current-owner checks or claim-based 2020–2024 shares.
- **Decision:** investigate routing and switching first as possible exposures.

## 4. The candidate universe isn't a verified portfolio

- **Evidence:** [19,873 families with grant evidence and 5,595 families with a recent application and no grant detected](../02-methodology/candidate-portfolio-universe.md), with no verified active rights or current owners yet. The [saved US recount](../03-market-and-patent-analysis/patent-landscape.md#where-nokias-patents-came-from) verifies 36,630 distinct publications and 37,710 owner-publication listings. Origin counts overlap, so a distinct Alcatel/Lucent share awaits a corrected publication-level SQL rerun.
- **Confidence:** high that it isn't verified. The size of the gap is unknown.
- **What would change it:** register checks.
- **Decision:** base the [cost model](../04-financial-analysis/ten-year-maintenance-cost-model.md) on verified sampled rights, not on these counts.

## 5. Market leadership differs by segment

- **Evidence:** [segment figures](../03-market-and-patent-analysis/market-context-and-peer-selection.md#segment-figures-behind-the-map): Huawei and Ciena lead in optical transport, Cisco in routers and all Ethernet switching, NVIDIA in data centre Ethernet, and Celestica in Ethernet AI back-end.
- **Confidence:** high for the published figures, with some from trade coverage of paid reports.
- **What would change it:** new market reports, as periods differ.
- **Decision:** compare by technology, not by company total.
