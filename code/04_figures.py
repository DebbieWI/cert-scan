#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: draws the two figures from the release table.
  Figure 1 (paper/figures/fig1_tilemap.png): a tile map of all 52 jurisdictions,
    one panel for drinking water and one for wastewater, shaded by status.
  Figure 2 (paper/figures/fig2_timeline.png): when each cybersecurity provision
    took effect, from Pennsylvania 2010 to New York 2026.
Figures carry a DRAFT stamp until the author has verified the data; run with
--final to remove it.
Do you need to open it? No. Open the PNG files.
"""
import csv, sys
from datetime import date
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/processed/cert_scan_v1.csv"
OUT = ROOT / "paper/figures"
FINAL = "--final" in sys.argv

# Ordinal single-hue ramp (validated: dataviz validate_palette --ordinal, light) + neutral for "none"
COL = {"required": "#184f95", "credited_optional": "#3987e5", "general_security_only": "#86b6ef",
       "no_provision_found": "#e4e3df", "unknown": "#e4e3df"}
LABEL = {"required": "Required by statute or regulation", "credited_optional": "Credited, not required",
         "general_security_only": "General security course required (cyber content unconfirmed)",
         "no_provision_found": "No provision found"}
INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": INK,
                     "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2})

# Standard US tile-grid layout (col, row), plus DC and PR
GRID = {"AK": (0, 0), "ME": (11, 0), "VT": (10, 1), "NH": (11, 1), "WA": (1, 2), "ID": (2, 2), "MT": (3, 2),
        "ND": (4, 2), "MN": (5, 2), "IL": (6, 2), "WI": (7, 2), "MI": (8, 2), "NY": (9, 2), "MA": (10, 2),
        "RI": (11, 2), "OR": (1, 3), "NV": (2, 3), "WY": (3, 3), "SD": (4, 3), "IA": (5, 3), "IN": (6, 3),
        "OH": (7, 3), "PA": (8, 3), "NJ": (9, 3), "CT": (10, 3), "CA": (1, 4), "UT": (2, 4), "CO": (3, 4),
        "NE": (4, 4), "MO": (5, 4), "KY": (6, 4), "WV": (7, 4), "VA": (8, 4), "MD": (9, 4), "DE": (10, 4),
        "AZ": (2, 5), "NM": (3, 5), "KS": (4, 5), "AR": (5, 5), "TN": (6, 5), "NC": (7, 5), "SC": (8, 5),
        "DC": (9, 5), "OK": (4, 6), "LA": (5, 6), "MS": (6, 6), "AL": (7, 6), "GA": (8, 6), "HI": (0, 7),
        "TX": (4, 7), "FL": (9, 7), "PR": (11, 7)}


def stamp(fig):
    if not FINAL:
        fig.text(0.99, 0.01, "DRAFT - not verified", ha="right", va="bottom", fontsize=8, color="#d03b3b")


def tilemap(rows):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), facecolor=SURF)
    for ax, pg, title in zip(axes, ("drinking_water", "wastewater"), ("Drinking water", "Wastewater")):
        ax.set_facecolor(SURF)
        status = {r["abbr"]: r for r in rows if r["program"] == pg}
        for ab, (c, rr) in GRID.items():
            r = status[ab]
            s = r["cyber_status"]
            fc = COL[s]
            ax.add_patch(FancyBboxPatch((c + 0.06, -rr + 0.06), 0.88, 0.88,
                                        boxstyle="round,pad=0,rounding_size=0.08",
                                        fc=fc, ec=SURF, lw=2))
            if r["confidence"] == "low":   # unconfirmed: dashed outline
                ax.add_patch(FancyBboxPatch((c + 0.1, -rr + 0.1), 0.8, 0.8,
                                            boxstyle="round,pad=0,rounding_size=0.06",
                                            fc="none", ec=INK2, lw=0.9, ls=(0, (2, 2))))
            dark = s in ("required", "credited_optional")
            ax.text(c + 0.5, -rr + 0.5, ab, ha="center", va="center", fontsize=8.5,
                    color="#ffffff" if dark else INK, fontweight="bold" if s != "no_provision_found" else "normal")
        ax.set_xlim(-0.1, 12.1); ax.set_ylim(-7.2, 1.1); ax.set_aspect("equal"); ax.axis("off")
        n = {k: sum(1 for r in status.values() if r["cyber_status"] == k) for k in LABEL}
        ax.set_title(f"{title}: {n['required']} required, {n['credited_optional']} credited",
                     loc="left", fontsize=11, color=INK, pad=6)
    handles = [plt.Rectangle((0, 0), 1, 1, fc=COL[k], ec="none") for k in LABEL]
    handles.append(plt.Rectangle((0, 0), 1, 1, fc="none", ec=INK2, ls=(0, (2, 2))))
    fig.legend(handles, list(LABEL.values()) + ["Dashed outline: source not yet confirmed"],
               loc="lower center", ncol=3, frameon=False, fontsize=8.5)
    fig.suptitle("Cybersecurity in U.S. water operator certification, October 2026",
                 x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.text(0.01, 0.905, "Codified rule status per jurisdiction (50 states, DC, Puerto Rico). Source: CERT-SCAN v1.0 draft.",
             fontsize=8.5, color=INK2)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.84, bottom=0.12, wspace=0.05)
    stamp(fig)
    fig.savefig(OUT / "fig1_tilemap.png", dpi=200, facecolor=SURF)
    plt.close(fig)


def parse(d):
    d = d.split(" ")[0]
    parts = [int(x) for x in d.split("-") if x.isdigit()]
    return date(parts[0], parts[1] if len(parts) > 1 else 7, parts[2] if len(parts) > 2 else 1)


def timeline(rows):
    ev = {}
    for r in rows:
        if r["cyber_status"] in ("required", "credited_optional", "general_security_only") and r["effective_date"]:
            key = (r["abbr"], r["cyber_status"], r["effective_date"].split(" ")[0])
            ev.setdefault(key, []).append("DW" if r["program"] == "drinking_water" else "WW")
    raw = sorted(((parse(k[2]), k[0], k[1], "+".join(sorted(v))) for k, v in ev.items()))
    # Merge same-state, same-status events less than 60 days apart into one label (e.g. NY DW + NY WW)
    items = []
    for d, ab, s, pgs in raw:
        prev = next((i for i, it in enumerate(items)
                     if it[1] == ab and it[2] == s and (d - it[0]).days < 60), None)
        if prev is not None:
            d0, _, _, lab = items[prev]
            items[prev] = (d0, ab, s, f"{lab} {d0:%b %-d},\n{pgs} {d:%b %-d}")
        else:
            items.append((d, ab, s, pgs))
    items.sort()
    fig, ax = plt.subplots(figsize=(11, 4.0), facecolor=SURF)
    ax.set_facecolor(SURF)
    ax.axhline(0, color=INK2, lw=1, zorder=1)
    up, down = [0.6, 1.25], [-0.6, -1.25]
    nu = nd = 0
    for d, ab, s, pgs in items:
        go_up = (nu <= nd)
        y = up[nu % 2] if go_up else down[nd % 2]
        if go_up: nu += 1
        else: nd += 1
        ax.plot([d, d], [0, y], color=INK2, lw=0.8, zorder=1)
        ax.scatter([d], [0], s=70, color=COL[s], edgecolor=SURF, linewidth=2,
                   zorder=5 if s == "required" else 3)
        lab =f"{ab} {pgs}\n{d:%Y}" if "," in pgs else f"{ab} {pgs}\n{d:%b %Y}"
        ax.text(d, y + (0.08 if y > 0 else -0.08), lab, ha="center",
                va="bottom" if y > 0 else "top", fontsize=8, color=INK)
    ax.set_ylim(-2.0, 2.0); ax.set_yticks([])
    ax.set_xlim(date(2009, 6, 1), date(2027, 6, 1))
    for sp in ("left", "right", "top"):
        ax.spines[sp].set_visible(False)
    handles = [plt.Line2D([], [], marker="o", ls="", ms=8, color=COL[k]) for k in
               ("required", "credited_optional", "general_security_only")]
    ax.legend(handles, [LABEL[k] for k in ("required", "credited_optional", "general_security_only")],
              loc="upper left", bbox_to_anchor=(0.0, 1.08), ncol=3, frameon=False, fontsize=8.5)
    ax.set_title("When cybersecurity entered operator certification", loc="left", fontsize=12,
                 fontweight="bold", color=INK, pad=26)
    fig.text(0.01, 0.01, "Effective dates of provisions in CERT-SCAN. DW = drinking water, WW = wastewater. "
             "Maine and Massachusetts dates are the guidance or approval dates.", fontsize=7.5, color=INK2)
    fig.subplots_adjust(left=0.03, right=0.98, top=0.84, bottom=0.13)
    stamp(fig)
    fig.savefig(OUT / "fig2_timeline.png", dpi=200, facecolor=SURF)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(DATA, encoding="utf-8")))
    tilemap(rows); timeline(rows)
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))


if __name__ == "__main__":
    main()
