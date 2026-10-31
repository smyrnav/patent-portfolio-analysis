"""Draw the map of who leads each AI and cloud networking segment."""
from pathlib import Path

import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "docs/img/ai_cloud_leaders.png"
ACCENT, NOKIA, CELL, EMPTY, INK, MUTED = "#124191", "#FFC000", "#DCE3EF", "#F5F6F8", "#1A1A1A", "#6B7686"
companies = ["Nokia", "Ciena", "Cisco", "Arista", "Huawei", "NVIDIA", "Celestica"]
rows = [
    ("Optical transport\nrevenue rank, 2025", {"Huawei": "#1", "Ciena": "#2", "Nokia": "#3", "Cisco": "#5"}, "Huawei"),
    ("Data centre interconnect\ntop three, 2025", {"Ciena": "Top 3*", "Nokia": "Top 3", "Cisco": "Top 3"}, "Ciena"),
    ("Routers\nshare, 2Q 2026", {"Cisco": "34.7%", "Huawei": "29.9%", "Nokia": "Not stated"}, "Cisco"),
    ("All Ethernet switching\nshare, 2Q 2026", {"Cisco": "28.7%", "Arista": "13.4%", "Huawei": "8.2%"}, "Cisco"),
    ("Data centre Ethernet\nshare, 2Q 2026", {"NVIDIA": "20.4%", "Arista": "18.7%", "Cisco": "18.2%"}, "NVIDIA"),
    ("Ethernet AI back-end\nrank, 2Q 2026", {"Celestica": "#1", "NVIDIA": "#2", "Arista": "#3", "Cisco": "#4"}, "Celestica"),
]
fig, ax = plt.subplots(figsize=(13.5, 7.4))
ax.set_xlim(-2.45, len(companies))
ax.set_ylim(len(rows) + .25, -1.35)
ax.axis("off")
ax.text(-2.45, -1.05, "No single company leads AI and cloud networking", fontsize=19, fontweight="bold", color=INK)
ax.text(-2.45, -.68, "Dark blue marks the leader of each segment, and yellow marks Nokia. Blank means no figure in the sources I checked.", fontsize=11, color=MUTED)
for c, name in enumerate(companies):
    ax.text(c + .5, -.2, name, ha="center", fontsize=12.5, fontweight="bold", color=INK)
for r, (label, values, leader) in enumerate(rows):
    ax.text(-2.4, r + .5, label, va="center", fontsize=11.5, color=INK)
    for c, name in enumerate(companies):
        value = values.get(name, "")
        fill = ACCENT if name == leader else NOKIA if name == "Nokia" and value else CELL if value else EMPTY
        ink = "white" if name == leader else INK
        ax.add_patch(plt.Rectangle((c + .03, r + .05), .94, .9, fc=fill, ec="none"))
        ax.text(c + .5, r + .5, value, ha="center", va="center", fontsize=12, fontweight="bold" if value else "normal", color=ink)
ax.text(-2.45, len(rows) + .18, "*Ciena's own deck cites Dell'Oro for #1, excluding China. Sources: IDC, Dell'Oro and trade reports of Dell'Oro. Measures differ, so compare within a row, not between rows.", fontsize=10, color=MUTED)
fig.tight_layout(pad=.5)
fig.savefig(OUT, dpi=150)
