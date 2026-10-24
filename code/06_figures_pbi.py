#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: draws the preprint's figures in a Power BI-style look
(white visual cards on a light canvas, Inter font, KPI cards, data labels,
light gridlines). Every figure reads data/processed/cert_scan_v1.csv or the
exam-outline scan, so the figures cannot disagree with the table.
Palettes were checked with the dataviz validator:
  status (ordinal, one hue): #6AAFFF -> #118DFF -> #12239E, plus neutral gray for "none"
  program (categorical, 2 slots): drinking water #118DFF, wastewater #E66C37
Outputs: paper/figures/pbi_*.png (300 dpi). Run with --final to remove the
DRAFT tag. Do you need to open it? No. Open the PNG files.
"""
import csv, re, sys
from collections import Counter
from datetime import date
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/processed/cert_scan_v1.csv"
NTK = ROOT / "data/raw/exam_ntk/2025"
OUT = ROOT / "paper/figures"
FINAL = "--final" in sys.argv

CANVAS, CARD, BORDER = "#F3F2F1", "#FFFFFF", "#E1DFDD"
INK, INK2, INK3, GRID = "#252423", "#605E5C", "#8A8886", "#EDEBE9"
STATUS = {"required": "#12239E", "credited_optional": "#118DFF", "general_security_only": "#6AAFFF",
          "no_provision_found": "#E1DFDD"}
SLABEL = {"required": "Required", "credited_optional": "Credited, not required",
          "general_security_only": "General security only", "no_provision_found": "No provision found"}
PROG = {"drinking_water": "#118DFF", "wastewater": "#E66C37"}
PLABEL = {"drinking_water": "Drinking water", "wastewater": "Wastewater"}

for f in font_manager.findSystemFonts():
    if "Inter" in Path(f).name:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Inter", "font.size": 7.5, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.edgecolor": BORDER, "axes.linewidth": 0.6})

GRID_POS = {"AK": (0, 0), "ME": (11, 0), "VT": (10, 1), "NH": (11, 1), "WA": (1, 2), "ID": (2, 2), "MT": (3, 2),
            "ND": (4, 2), "MN": (5, 2), "IL": (6, 2), "WI": (7, 2), "MI": (8, 2), "NY": (9, 2), "MA": (10, 2),
            "RI": (11, 2), "OR": (1, 3), "NV": (2, 3), "WY": (3, 3), "SD": (4, 3), "IA": (5, 3), "IN": (6, 3),
            "OH": (7, 3), "PA": (8, 3), "NJ": (9, 3), "CT": (10, 3), "CA": (1, 4), "UT": (2, 4), "CO": (3, 4),
            "NE": (4, 4), "MO": (5, 4), "KY": (6, 4), "WV": (7, 4), "VA": (8, 4), "MD": (9, 4), "DE": (10, 4),
            "AZ": (2, 5), "NM": (3, 5), "KS": (4, 5), "AR": (5, 5), "TN": (6, 5), "NC": (7, 5), "SC": (8, 5),
            "DC": (9, 5), "OK": (4, 6), "LA": (5, 6), "MS": (6, 6), "AL": (7, 6), "GA": (8, 6), "HI": (0, 7),
            "TX": (4, 7), "FL": (9, 7), "PR": (11, 7)}


def card(fig, rect, title=None, subtitle=None):
    """A Power BI visual container: white card with thin border, title top-left."""
    x, y, w, h = rect
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.006",
                                      transform=fig.transFigure, fc=CARD, ec=BORDER, lw=0.7, zorder=-1))
    if title:
        fig.text(x + 0.012, y + h - 0.018, title, fontsize=9, fontweight="semibold", color=INK, va="top")
    if subtitle:
        fig.text(x + 0.012, y + h - 0.018 - 0.045 * (4.0 / fig.get_figheight()), subtitle,
                 fontsize=7, color=INK2, va="top")


def stamp(fig):
    if not FINAL:
        fig.text(0.995, 0.004, "DRAFT", ha="right", va="bottom", fontsize=6.5, color="#D64550")


def style_axes(ax, xgrid=True):
    ax.set_facecolor(CARD)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.tick_params(length=0)


def legend_row(fig, x, y, items, fs=7):
    for label, col in items:
        fig.patches.append(matplotlib.patches.Circle((x, y), 0.0042 * 12 / fig.get_figwidth(),
                                                     transform=fig.transFigure, fc=col, ec="none"))
        t = fig.text(x + 0.012 * 7 / fig.get_figwidth() * 1.4, y, label, fontsize=fs, color=INK2, va="center")
        x += 0.02 * 7 / fig.get_figwidth() * 1.4 + len(label) * 0.0072 * 7 / fig.get_figwidth()


def load():
    return list(csv.DictReader(open(DATA, encoding="utf-8")))


# ---------------------------------------------------------------- Figure 1
def fig_dashboard(rows):
    fig = plt.figure(figsize=(7.2, 4.9), facecolor=CANVAS)
    fig.patches.append(Rectangle((0, 0.935), 1, 0.065, transform=fig.transFigure, fc="#12239E", ec="none"))
    fig.text(0.015, 0.967, "CERT-SCAN  |  Cybersecurity in water operator certification", color="white",
             fontsize=10.5, fontweight="semibold", va="center")
    fig.text(0.985, 0.967, "52 jurisdictions  ·  data as of 23 Oct 2026", color="#DCE6FF", fontsize=7.5,
             ha="right", va="center")
    juris = {s: sorted({r["abbr"] for r in rows if r["cyber_status"] == s}) for s in STATUS}
    wt = sum(1 for r in rows if r["program"] == "drinking_water" and r["exam_cyber_content"].startswith("yes"))
    kpis = [(str(len({r['abbr'] for r in rows})), "Jurisdictions coded", INK),
            (str(len(juris["required"])), "Require cyber training", STATUS["required"]),
            (str(len(juris["credited_optional"])), "Credit it, not required", STATUS["credited_optional"]),
            (str(len(juris["general_security_only"])), "General security course", "#3C8FE0"),
            (str(wt), "Exams list a cyber task", INK)]
    w, gap, x0 = 0.186, 0.0105, 0.012
    for i, (num, lab, col) in enumerate(kpis):
        x = x0 + i * (w + gap)
        card(fig, (x, 0.765, w, 0.15))
        fig.text(x + w / 2, 0.86, num, ha="center", va="center", fontsize=20, fontweight="semibold", color=col)
        fig.text(x + w / 2, 0.79, lab, ha="center", va="center", fontsize=7, color=INK2)
    for j, pg in enumerate(("drinking_water", "wastewater")):
        x = 0.012 + j * 0.4935
        n = Counter(r["cyber_status"] for r in rows if r["program"] == pg)
        card(fig, (x, 0.09, 0.4815, 0.655), f"{PLABEL[pg]} certification",
             f"{n['required']} required · {n['credited_optional']} credited · "
             f"{n['general_security_only']} general security · {n['no_provision_found']} none found")
        ax = fig.add_axes((x + 0.012, 0.105, 0.4575, 0.545))
        ax.set_facecolor(CARD); ax.axis("off")
        st = {r["abbr"]: r for r in rows if r["program"] == pg}
        for ab, (c, rr) in GRID_POS.items():
            r = st[ab]; s = r["cyber_status"]
            ax.add_patch(Rectangle((c + 0.05, -rr + 0.05), 0.9, 0.9, fc=STATUS[s], ec=CARD, lw=1.2))
            if r["confidence"] == "low":
                ax.add_patch(Rectangle((c + 0.12, -rr + 0.12), 0.76, 0.76, fc="none", ec=INK2, lw=0.6,
                                       ls=(0, (2, 1.5))))
            ax.text(c + 0.5, -rr + 0.5, ab, ha="center", va="center", fontsize=6.3,
                    color="white" if s in ("required", "credited_optional") else INK,
                    fontweight="semibold" if s != "no_provision_found" else "normal")
        ax.set_xlim(-0.05, 12.05); ax.set_ylim(-7.1, 1.05); ax.set_aspect("equal")
    x = 0.02
    for s in STATUS:
        fig.patches.append(Rectangle((x, 0.035), 0.014, 0.022, transform=fig.transFigure, fc=STATUS[s], ec="none"))
        fig.text(x + 0.019, 0.046, SLABEL[s], fontsize=7, color=INK2, va="center")
        x += 0.035 + len(SLABEL[s]) * 0.0078
    fig.patches.append(Rectangle((x, 0.035), 0.014, 0.022, transform=fig.transFigure, fc="none", ec=INK2,
                                 ls=(0, (2, 1.5)), lw=0.6))
    fig.text(x + 0.019, 0.046, "Awaiting agency confirmation", fontsize=7, color=INK2, va="center")
    stamp(fig)
    fig.savefig(OUT / "pbi_fig1_dashboard.png", dpi=300, facecolor=CANVAS)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 2
def fig_status_by_program(rows):
    fig = plt.figure(figsize=(3.4, 2.5), facecolor=CANVAS)
    card(fig, (0.02, 0.03, 0.96, 0.94), "Records by status and program", "Count of jurisdictions (n = 52 each)")
    ax = fig.add_axes((0.36, 0.13, 0.57, 0.6)); style_axes(ax)
    cats = list(SLABEL)
    import numpy as np
    y = np.arange(len(cats)); h = 0.36
    for k, pg in enumerate(("drinking_water", "wastewater")):
        c = Counter(r["cyber_status"] for r in rows if r["program"] == pg)
        vals = [c[s] for s in cats]
        bars = ax.barh(y + (k - 0.5) * h * 1.08, vals, height=h, color=PROG[pg], label=PLABEL[pg])
        for b, v in zip(bars, vals):
            ax.text(b.get_width() + 0.8, b.get_y() + b.get_height() / 2, str(v), va="center", fontsize=6.5, color=INK)
    ax.set_yticks(y, [SLABEL[s] for s in cats], fontsize=7, color=INK); ax.invert_yaxis()
    ax.set_xlim(0, 55); ax.set_xticks([0, 10, 20, 30, 40, 50])
    lg = ax.legend(loc="upper right", frameon=False, fontsize=6.5, handlelength=0.8, handleheight=0.8)
    stamp(fig)
    fig.savefig(OUT / "pbi_fig2_status_by_program.png", dpi=300, facecolor=CANVAS)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 3
def parse(d):
    p = [int(x) for x in d.split(" ")[0].split("-") if x.isdigit()]
    return date(p[0], p[1] if len(p) > 1 else 7, p[2] if len(p) > 2 else 1)


def fig_timeline(rows):
    ev = {}
    for r in rows:
        if r["cyber_status"] in ("required", "credited_optional", "general_security_only") and r["effective_date"]:
            ev.setdefault((r["abbr"], r["cyber_status"], r["effective_date"].split(" ")[0]), []).append(
                "DW" if r["program"] == "drinking_water" else "WW")
    raw = sorted((parse(k[2]), k[0], k[1], "+".join(sorted(v))) for k, v in ev.items())
    items = []
    for d, ab, s, pg in raw:
        prev = next((i for i, it in enumerate(items) if it[1] == ab and it[2] == s and (d - it[0]).days < 60), None)
        if prev is not None:
            d0, _, _, lab = items[prev]
            items[prev] = (d0, ab, s, f"{lab} {d0:%b %-d}\n{pg} {d:%b %-d}")
        else:
            items.append((d, ab, s, pg))
    items.sort()
    fig = plt.figure(figsize=(7.2, 2.6), facecolor=CANVAS)
    card(fig, (0.01, 0.03, 0.98, 0.94), "When cybersecurity entered operator certification",
         "Effective date of each provision, by status")
    ax = fig.add_axes((0.03, 0.12, 0.94, 0.62)); style_axes(ax, xgrid=False)
    ax.axhline(0, color=INK3, lw=0.8)
    up, down = [0.5, 1.35], [-0.5, -1.35]; nu = nd = 0
    for d, ab, s, pg in items:
        go = nu <= nd
        yv = up[nu % 2] if go else down[nd % 2]
        nu, nd = (nu + 1, nd) if go else (nu, nd + 1)
        ax.plot([d, d], [0, yv], color=BORDER, lw=0.9, zorder=1)
        ax.scatter([d], [0], s=46, color=STATUS[s], edgecolor=CARD, lw=1.4, zorder=5 if s == "required" else 3)
        lab = f"{ab}  {pg}" + ("" if "\n" in pg else f"\n{d:%b %Y}")
        ax.text(d, yv + (0.07 if yv > 0 else -0.07), lab, ha="center", va="bottom" if yv > 0 else "top",
                fontsize=6.5, color=INK, linespacing=1.15)
    ax.set_ylim(-2.2, 2.25); ax.set_yticks([])
    ax.set_xlim(date(2009, 6, 1), date(2027, 3, 1))
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    x = 0.5
    for s in ("required", "credited_optional", "general_security_only"):
        fig.patches.append(matplotlib.patches.Circle((x, 0.875), 0.006, transform=fig.transFigure, fc=STATUS[s]))
        fig.text(x + 0.012, 0.875, SLABEL[s], fontsize=6.8, color=INK2, va="center")
        x += 0.03 + len(SLABEL[s]) * 0.0062
    stamp(fig)
    fig.savefig(OUT / "pbi_fig3_timeline.png", dpi=300, facecolor=CANVAS)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 4
def exam_matrix():
    areas = [("Water treatment", "Water-Treatment-Class-{}_mh-fin.txt"),
             ("Water distribution", "WaterDistribution---Class-{}_mh-fin.txt"),
             ("Wastewater treatment", "WastewaterTreatment---Class-{}_mh-fin.txt"),
             ("Wastewater collection", "Collection---Class-{}_final.txt")]
    m = []
    for name, pat in areas:
        row = []
        for c in range(1, 5):
            t = (NTK / pat.format(c)).read_text(errors="ignore")
            row.append(bool(re.search(r"cyber", t, re.I)))
        m.append((name, row))
    return m


def fig_exam_matrix():
    m = exam_matrix()
    fig = plt.figure(figsize=(3.4, 2.25), facecolor=CANVAS)
    card(fig, (0.02, 0.03, 0.96, 0.94), "Cybersecurity task in 2025 WPI exam outlines",
         "Need-to-know criteria, classes 1 to 4")
    ax = fig.add_axes((0.36, 0.08, 0.6, 0.62)); ax.set_facecolor(CARD); ax.axis("off")
    for j in range(4):
        ax.text(j + 0.5, 4.25, f"Class {j + 1}", ha="center", va="center", fontsize=7, color=INK2,
                fontweight="semibold")
    for i, (name, row) in enumerate(m):
        yv = 3 - i
        fig.text(0.355, 0.08 + 0.62 * (yv + 0.5) / 4.6, name, ha="right", va="center", fontsize=7, color=INK)
        for j, v in enumerate(row):
            ax.add_patch(Rectangle((j + 0.04, yv + 0.06), 0.92, 0.88, fc="#12239E" if v else "#F3F2F1",
                                   ec=CARD, lw=1))
            ax.text(j + 0.5, yv + 0.5, "Listed" if v else "None", ha="center", va="center", fontsize=6.6,
                    color="white" if v else INK3, fontweight="semibold" if v else "normal")
    ax.set_xlim(0, 4); ax.set_ylim(0, 4.6)
    stamp(fig)
    fig.savefig(OUT / "pbi_fig4_exam_matrix.png", dpi=300, facecolor=CANVAS)
    plt.close(fig)
    return m


# ---------------------------------------------------------------- Figure 5
def fig_exam_coverage(rows):
    fig = plt.figure(figsize=(3.4, 2.2), facecolor=CANVAS)
    card(fig, (0.02, 0.03, 0.96, 0.94), "Who writes the exam?", "Programs by exam source and cyber content")
    ax = fig.add_axes((0.33, 0.2, 0.6, 0.48)); style_axes(ax)
    def bucket(r):
        e = r["exam_cyber_content"]
        if e.startswith("yes"):
            return "WPI, cyber task listed"
        if r["exam_provider"].startswith("WPI"):
            return "WPI, no cyber task"
        return "Other or state exam"
    cats = ["WPI, cyber task listed", "WPI, no cyber task", "Other or state exam"]
    cols = {"WPI, cyber task listed": "#12239E", "WPI, no cyber task": "#118DFF", "Other or state exam": "#C8C6C4"}
    left = {"drinking_water": 0, "wastewater": 0}
    yl = {"drinking_water": 1, "wastewater": 0}
    for cat in cats:
        for pg in ("drinking_water", "wastewater"):
            v = sum(1 for r in rows if r["program"] == pg and bucket(r) == cat)
            if v:
                ax.barh(yl[pg], v, left=left[pg], height=0.55, color=cols[cat], ec=CARD, lw=1)
                if v >= 3:
                    ax.text(left[pg] + v / 2, yl[pg], str(v), ha="center", va="center", fontsize=7,
                            color="white" if cat != "Other or state exam" else INK, fontweight="semibold")
                left[pg] += v
    ax.set_yticks([1, 0], ["Drinking water", "Wastewater"], fontsize=7, color=INK)
    ax.set_xlim(0, 52); ax.set_xticks([0, 13, 26, 39, 52])
    fig.text(0.06, 0.035, "One drinking water program (NM) uses WPI only for distribution.", fontsize=6,
             color=INK3)
    x = 0.06
    for cat in cats:
        fig.patches.append(Rectangle((x, 0.755), 0.025, 0.04, transform=fig.transFigure, fc=cols[cat]))
        fig.text(x + 0.033, 0.775, cat, fontsize=6.3, color=INK2, va="center")
        x += 0.07 + len(cat) * 0.0118
    stamp(fig)
    fig.savefig(OUT / "pbi_fig5_exam_coverage.png", dpi=300, facecolor=CANVAS)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 6
def fig_instrument(rows):
    pos = [r for r in rows if r["cyber_status"] != "no_provision_found"]
    names = {"statute": "Statute", "regulation": "Regulation", "guidance": "Agency guidance",
             "board_practice": "Board course approvals"}
    c = Counter(r["instrument_type"] for r in pos)
    fig = plt.figure(figsize=(3.4, 2.2), facecolor=CANVAS)
    card(fig, (0.02, 0.03, 0.96, 0.94), "What kind of rule stands behind it?",
         f"Instrument type, {len(pos)} records with a provision")
    ax = fig.add_axes((0.36, 0.22, 0.56, 0.46)); style_axes(ax)
    keys = [k for k in ("statute", "regulation", "guidance", "board_practice") if c[k]]
    vals = [c[k] for k in keys]
    cols = ["#12239E" if k in ("statute", "regulation") else "#118DFF" for k in keys]
    bars = ax.barh(range(len(keys)), vals, color=cols, height=0.55)
    for b, v in zip(bars, vals):
        ax.text(v + 0.15, b.get_y() + b.get_height() / 2, str(v), va="center", fontsize=7, color=INK)
    ax.set_yticks(range(len(keys)), [names[k] for k in keys], fontsize=7, color=INK); ax.invert_yaxis()
    ax.set_xlim(0, max(vals) + 1.5)
    fig.text(0.06, 0.035, "Dark: codified (statute or regulation). Light: guidance or practice.", fontsize=6,
             color=INK3)
    stamp(fig)
    fig.savefig(OUT / "pbi_fig6_instrument.png", dpi=300, facecolor=CANVAS)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 7
def fig_evidence(rows):
    fig = plt.figure(figsize=(3.4, 2.0), facecolor=CANVAS)
    card(fig, (0.02, 0.03, 0.96, 0.94), "Evidence behind each record", "Confidence level by program")
    ax = fig.add_axes((0.28, 0.14, 0.66, 0.5)); style_axes(ax)
    lv = [("high", "Primary legal text", "#12239E"), ("medium", "Agency document", "#118DFF"),
          ("low", "Awaiting confirmation", "#6AAFFF")]
    for yv, pg in ((1, "drinking_water"), (0, "wastewater")):
        left = 0
        c = Counter(r["confidence"] for r in rows if r["program"] == pg)
        for k, _, col in lv:
            v = c[k]
            if v:
                ax.barh(yv, v, left=left, height=0.55, color=col, ec=CARD, lw=1)
                if v >= 3:
                    ax.text(left + v / 2, yv, str(v), ha="center", va="center", fontsize=7, color="white",
                            fontweight="semibold")
                left += v
    ax.set_yticks([1, 0], ["Drinking water", "Wastewater"], fontsize=7, color=INK)
    ax.set_xlim(0, 52); ax.set_xticks([0, 13, 26, 39, 52])
    x = 0.06
    for _, lab, col in lv:
        fig.patches.append(Rectangle((x, 0.725), 0.025, 0.045, transform=fig.transFigure, fc=col))
        fig.text(x + 0.033, 0.747, lab, fontsize=6.3, color=INK2, va="center")
        x += 0.075 + len(lab) * 0.0128
    stamp(fig)
    fig.savefig(OUT / "pbi_fig7_evidence.png", dpi=300, facecolor=CANVAS)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load()
    fig_dashboard(rows); fig_status_by_program(rows); fig_timeline(rows)
    fig_exam_matrix(); fig_exam_coverage(rows); fig_instrument(rows); fig_evidence(rows)
    print("wrote", sorted(p.name for p in OUT.glob("pbi_*.png")))


if __name__ == "__main__":
    main()
