# US renewal break-even

A supporting calculation for one US patent's keep-or-drop decision. The main financial work is the [ten-year maintenance cost model](ten-year-maintenance-cost-model.md). Everything here is official US fees only, not filing or attorney costs.

## How much value must a patent generate to justify its next fee?

Using the [USPTO large-entity fees](../appendices/sources.md#patent-rules-and-data-sources), and the [median US time to grant of 4.05 years](../02-methodology/metrics.md#measured-so-far):

| Renewal | Fee | Cover it buys | Break-even value per year at 5% | At 10% | At 15% |
|---|---:|---:|---:|---:|---:|
| 3.5 years | $2,150 | 4 years | $606 | $678 | $753 |
| 7.5 years | $4,040 | 4 years | $1,139 | $1,275 | $1,415 |
| 11.5 years | $8,280 | 4.45 years | $2,121 | $2,395 | $2,682 |

The three fees total $14,470, or about $6,284 in present value at 10%. The discount rate and the value of each patent are assumptions, because public data doesn't show them.

## How mean and median fees would be worked out

Nokia's reports don't show patent costs, so these need official fees and renewal records. Until I have those records, this example shows how the calculation works, using assumed renewal rates:

| Share renewed at 3.5, 7.5 and 11.5 years (assumed) | Mean fees per patent | Median fees per patent |
|---|---:|---:|
| 90%, 80%, 70% | $9,017 | $14,470 |
| 80%, 60%, 40% | $5,249 | $2,150 |

The median can jump a long way with small changes, as fees come in large steps, so the mean and the full spread both matter. The rates are placeholders, not findings.

## An arithmetic illustration

If 1,000–1,300 US patents a year were each kept for their full term, official fees would reach about $14.5M–$18.8M a year once the portfolio is steady.

This only shows the arithmetic. The patent counts haven't been checked for ownership or live status, and every patent is assumed to renew. It isn't Nokia's spending, and I draw no conclusion from it about whether fees are material.
