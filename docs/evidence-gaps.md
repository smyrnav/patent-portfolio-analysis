# What I have and what I still need

Checked against the [central research question](research-design.md):

> How does Nokia's patent portfolio and associated investment position compare with the leading competitors in AI and cloud infrastructure networking, and what strategic and financial lessons can be identified?

## Evidence by part of the question

✅ have it · 🟡 partly · ❌ missing

| Part of the question | Evidence needed | Nokia | Rivals | What's missing |
|---|---|---|---|---|
| **Who to compare** | Market leaders by segment | ✅ [Checked](competitors.md) | ✅ [Checked](competitors.md) | Nothing essential |
| **Patent size and growth** | New families in optical and IP, by year | 🟡 Families exist, areas not defined | ❌ | Tested technology definitions, rival patent table |
| **Patent age** | Families reaching 20 years by 2036 | 🟡 Dates exist, areas not defined | ❌ | Same as above |
| **Market coverage** | Filings in the US, Europe, China and Japan | 🟡 [Totals exist](twenty-years.md), not by area | ❌ | Same as above |
| **What Infinera added** | Nokia with and without Infinera | 🟡 Names identified | N/A | Technology definitions, ownership check |
| **Live and owned patents** | Renewals and transfers | ❌ | ❌ | USPTO renewal and assignment records |
| **Investment: R&D** | R&D spending by year | ✅ [20 years](twenty-years.md) | 🟡 [Latest period](competitors.md#investment-position) | Earlier years for rivals, and Huawei's report |
| **Investment: AI and cloud** | Sales and orders | 🟡 [Latest quarter](competitors.md) | 🟡 [Latest period](competitors.md) | Earlier years, where reported |
| **Investment: patent cost** | Fees and renewal behaviour | 🟡 US fees and [rough check](strategy.md#early-answer-are-fees-big-enough-to-matter) | ❌ | Renewal rates, and fees for Europe, China and Japan |
| **Strategic lessons** | Findings tied to decisions | ❌ | ❌ | Depends on everything above |
| **Financial lessons** | Budget scenarios and sensitivity | ❌ | N/A | Depends on costs and renewal rates |

## What to collect, in order

| # | Step | Why | Who | Cost |
|---|---|---|---|---|
| 1 | Clean rival owner names, and build a rival patent table | The sample has to cover each company | Me | Check size first |
| 2 | Pilot, freeze and test the [technology codebook](classification-codebook.md) | Everything else depends on it | Claude first, then I label and settle disagreements | Claims up to 119 GB, or Google Patents pages for free |
| 3 | Pull earlier R&D from rivals' annual reports | Shows the investment trend | Me, from SEC filings and Huawei's report | Free |
| 4 | Get USPTO renewal records | Live patents, renewal rates and costs, for rivals too | **You sign in**, then me | Free |
| 5 | Run the register spot-check on [the 35-patent sample](../data/processed/spot_check_sample.csv) | Shows the error rate | Me, with you reviewing | Free |
| 6 | Collect European, Chinese and Japanese fees | Completes the cost model | Me | Free |
| 7 | Test the four hypotheses, and build the gap map | Answers the patent comparison | Me, with your decisions | Small |
| 8 | Build the budget scenarios and sensitivity test | Financial lessons | Me, with your decisions | None |
| 9 | Write the decision brief | The final answer | You and me | None |

## What I can drop

| Item | Why |
|---|---|
| ETSI declarations | Optical and IP comparison doesn't depend on them. They matter for licensing and AI-RAN, so they can wait |
| AI-RAN, 6G and licensing database | Later extensions, only if the main question gets answered |
| Business units other than Optical and IP | Outside the question for now |
| More annual report extraction for Nokia | Enough for now, apart from checking the figures |

## What can't be answered from public data

| Gap | How the answer handles it |
|---|---|
| Nokia's and rivals' patent budgets | Estimates from fees and labelled assumptions |
| Value of individual patents | Scenarios and indicators, never stated as fact |
| Technical quality of products | Stated as out of scope |
| Current ownership outside the US | Stated as a limit, unless a free source turns up |

## Minimum for a defensible answer

Before 30 November, the essentials are steps 1–5 and 7, plus a simple version of steps 8 and 9 using US costs. European, Chinese and Japanese fees can be shown as a stated gap if there's no time.
