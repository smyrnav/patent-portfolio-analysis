"""Rerun every local step: cleaning, scoring, checks and tests. Add --charts to redraw the charts (needs matplotlib).

BigQuery steps can't run here. See sql/README.md.
"""
import subprocess
import sys

from common import ROOT

STEPS = ["clean_owners.py", "clean_lineage.py", "score_validation.py", "check_outputs.py"]
CHARTS = ["make_charts.py", "make_data_map.py", "make_universe_chart.py", "make_twenty_years_chart.py", "make_competitor_chart.py", "make_commercial_chart.py"]

for script in STEPS + (CHARTS if "--charts" in sys.argv else []):
    print(f"--- {script}")
    subprocess.run([sys.executable, str(ROOT / "src" / script)], check=True)
print("--- tests")
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], check=True, cwd=ROOT)
print("Everything passed.")
