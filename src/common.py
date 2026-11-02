"""Shared helpers for the project's scripts."""
import csv
import math
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def config():
    with (ROOT / "config/research_parameters.toml").open("rb") as f:
        return tomllib.load(f)


def rows(path):
    with (ROOT / path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(path, fields, records):
    with (ROOT / path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(records)


def wilson(matches, n, z=1.96):
    """95% Wilson range for a share of matches out of n."""
    p = matches / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return centre - half, centre + half


def cohen_kappa(pairs):
    """Cohen's kappa for a list of (label_a, label_b) pairs."""
    n = len(pairs)
    observed = sum(a == b for a, b in pairs) / n
    labels = {x for pair in pairs for x in pair}
    expected = sum(sum(a == l for a, _ in pairs) * sum(b == l for _, b in pairs) for l in labels) / (n * n)
    return (observed - expected) / (1 - expected) if expected < 1 else 1.0
