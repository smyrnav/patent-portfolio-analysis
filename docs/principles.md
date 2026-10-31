# Working principles

The [traineeship posting](https://www.linkedin.com/jobs/view/4483030441) lists how it expects people to work. I use those points as the rules for this analysis, and record honestly where I'm not there yet.

Status is ✅ done, 🟡 partly done or ⬜ not started.

| What the posting asks for | How I apply it | Evidence so far | Status |
|---|---|---|---|
| **Can turn a vague question into a structured analysis** | Turn "how should the budget be allocated?" into defined deliverables | [Analysis strategy](strategy.md) | ✅ |
| **Writes down assumptions and tests which ones actually move the answer** | List every assumption, then test the main ones | [Assumption register](assumptions.md), grouped by decision, with five priorities to test. Most aren't tested yet | 🟡 |
| **Gets curious when something looks strange and follows the trail until it makes sense** | Investigate numbers that don't fit | The [8,808 missing patents](questions.md#q14-did-my-first-two-searches-miss-older-us-patents), and 72,207 families against Nokia's 20,000+ | ✅ |
| **Builds work that others can rerun, understand, and improve** | Save exact queries, results and scripts, and explain each step | [`sql/`](../sql), [`data/`](../data), [`src/`](../src). The raw BigQuery results are partly hand-copied, and the all-years search is only saved in part | 🟡 |
| **Knows that reliable data needs both technical care and clear explanations** | Show where data comes from and how far it can be trusted | [Can I trust this data?](data-trust.md) and [fact checks](sources.md). The register spot-check isn't done yet | 🟡 |
| **Is comfortable with uncertainty and can explain a range with a probability curve** | Give ranges rather than single figures, and show a probability curve for the cost forecast | Break-even ranges so far. The Monte Carlo curve isn't built yet | ⬜ |
| **Makes numbers visible through clear charts, summaries, and presentations** | Lead with the finding, then the chart and limits | README charts and [data map](data-map.md). The decision brief isn't written yet | 🟡 |
| **Checks their own output before anyone else has to** | Run automatic checks before publishing, and compare against outside figures | [`src/check_outputs.py`](../src/check_outputs.py) | 🟡 |

## What I do at each step

1. **Before a query:** name the deliverable, decision, measure, what would change my mind and the data limit.
2. **While working:** add new assumptions to the [register](assumptions.md), and follow up anything strange.
3. **After a result:** save the exact query and result, then state how far it can be trusted.
4. **Before publishing:** run the checks, and read the output as a sceptical reviewer would.
5. **When presenting:** show key numbers as a chart or visual first, with the explanation short and underneath.

## Still to do

- Spot-check a random sample against official registers, and record the error rate
- Measure time to grant and renewal rates, replacing assumptions C8 and F1
- Build the cost forecast, with a sensitivity chart and a probability curve
- Export query results directly as CSV, so nothing is hand-copied
- Write the decision brief
