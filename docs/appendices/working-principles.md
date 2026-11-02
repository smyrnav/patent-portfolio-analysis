# Working principles

The [traineeship posting](https://www.linkedin.com/jobs/view/4483030441) lists how it expects people to work. I use those points as the rules for this analysis, and record honestly where I'm not there yet.

Status: ✅ done · 🟡 partly done · ❌ not started or missing.

| What the posting asks for | How I apply it | Evidence so far | Status |
|---|---|---|---|
| **Can turn a vague question into a structured analysis** | Turn the central question into five research questions and tests | [Research design](../01-research-design/research-design.md) | ✅ |
| **Writes down assumptions and tests which ones actually move the answer** | List every assumption, then test the main ones | [Assumptions](../04-financial-analysis/assumptions-and-scenarios.md), with five priorities to test. Most aren't tested yet | 🟡 |
| **Gets curious when something looks strange and follows the trail until it makes sense** | Investigate numbers that don't fit | The [8,808 missing patents](questions.md#q14-did-my-first-two-searches-miss-older-us-patents), and [patents showing other assignees](questions.md#q22-how-much-of-the-portfolio-i-attribute-to-nokia-does-it-still-own) | ✅ |
| **Builds work that others can rerun, understand, and improve** | Save exact queries, results and scripts, and explain each step | [`sql/`](../../sql/README.md), [`data/`](../../data), [`src/run_all.py`](../../src/run_all.py). Some raw BigQuery results are hand-copied, and the all-years search is only saved in part | 🟡 |
| **Knows that reliable data needs both technical care and clear explanations** | Show where data comes from and how far it can be trusted | [Data quality and lineage](../02-methodology/data-quality-and-lineage.md) and [fact checks](sources.md). The register spot-check isn't done yet | 🟡 |
| **Is comfortable with uncertainty and can explain a range with a probability curve** | Give ranges rather than single figures, and show a probability curve where a distribution can be justified | [Ranges on estimates](../03-market-and-patent-analysis/patent-landscape.md) and break-even. The curve isn't built yet | 🟡 |
| **Makes numbers visible through clear charts, summaries, and presentations** | Lead with the finding, then the chart and limits | README charts and [findings](../05-findings-and-recommendations/findings.md). The executive brief isn't written yet | 🟡 |
| **Checks their own output before anyone else has to** | Run automatic checks before publishing, and compare against outside figures | [`check_outputs.py`](../../src/check_outputs.py) and [`test_repository.py`](../../tests/test_repository.py) | ✅ |

## What I do at each step

1. **Before a query:** name the hypothesis or deliverable, decision, measure, what would change my mind and the data limit.
2. **While working:** add new assumptions to the [register](../04-financial-analysis/assumptions-and-scenarios.md), and follow up anything strange.
3. **After a result:** save the exact query and result, then state how far it can be trusted.
4. **Before publishing:** run [`src/run_all.py`](../../src/run_all.py), and read the output as a sceptical reviewer would.
5. **When presenting:** show key numbers as a chart or visual first, with the explanation short and underneath.
