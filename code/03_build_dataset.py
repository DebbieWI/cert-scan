#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: takes the hand-coded research file (data/coding/coding.csv,
one row per state and program, filled in from the sources) and the 2016 EPA
profiles, checks every row against the codebook rules, and writes the
release table data/processed/cert_scan_v1.csv plus a quality report
(data/processed/qa_report.txt) and the numbers file paper/stats.json.
Every number quoted in the README or paper comes from stats.json.
Do you need to open it? No. Open the outputs instead.

Run: python code/03_build_dataset.py
"""
import csv, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODING = ROOT / "data/coding/coding.csv"
PROFILES = ROOT / "data/processed/epa2016_state_profiles.csv"
OUT = ROOT / "data/processed/cert_scan_v1.csv"
QA = ROOT / "data/processed/qa_report.txt"
STATS = ROOT / "paper/stats.json"

JURIS = {
 "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado",
 "CT":"Connecticut","DE":"Delaware","DC":"District of Columbia","FL":"Florida","GA":"Georgia",
 "HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas",
 "KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts",
 "MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana",
 "NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico",
 "NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma",
 "OR":"Oregon","PA":"Pennsylvania","PR":"Puerto Rico","RI":"Rhode Island","SC":"South Carolina",
 "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia",
 "WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
PROGRAMS = ("drinking_water", "wastewater")
STATUS = ("required", "credited_optional", "general_security_only", "no_provision_found", "unknown")
INSTR = ("statute", "regulation", "emergency_rule", "board_practice", "guidance", "none")
CODIFIED = ("statute", "regulation", "emergency_rule")
REQUIRED_COLS = ["abbr", "program", "certifying_body", "program_authority_citation", "cyber_status",
                 "mechanism", "hours", "cycle_years", "recurring", "applies_to", "effective_date",
                 "instrument_type", "citation", "citation_url", "practice_beyond_rule",
                 "exam_provider", "exam_cyber_content", "evidence_note", "sources_searched",
                 "accessed", "confidence", "verified_by_author"]


def main():
    rows = list(csv.DictReader(open(CODING, newline="", encoding="utf-8")))
    profiles = {r["state"]: r for r in csv.DictReader(open(PROFILES, newline="", encoding="utf-8"))}
    problems, out = [], []
    seen = Counter((r["abbr"], r["program"]) for r in rows)

    for key, n in seen.items():
        if n > 1:
            problems.append(f"DUPLICATE {key} x{n}")
    for ab in JURIS:
        for pg in PROGRAMS:
            if (ab, pg) not in seen:
                problems.append(f"MISSING {ab} {pg}")

    for r in rows:
        tag = f"{r['abbr']}/{r['program']}"
        for c in REQUIRED_COLS:
            if c not in r:
                problems.append(f"{tag}: column {c} absent")
        if r["abbr"] not in JURIS:
            problems.append(f"{tag}: unknown jurisdiction")
        if r["cyber_status"] not in STATUS:
            problems.append(f"{tag}: bad status {r['cyber_status']}")
        if r["instrument_type"] not in INSTR:
            problems.append(f"{tag}: bad instrument {r['instrument_type']}")
        # Author decision 2: practice alone can never make a row 'required'
        if r["cyber_status"] in ("required", "general_security_only") and r["instrument_type"] not in CODIFIED:
            problems.append(f"{tag}: {r['cyber_status']} without a codified instrument (decision 2)")
        if r["cyber_status"] != "no_provision_found" and not r["citation_url"].startswith("http"):
            problems.append(f"{tag}: positive status needs a citation_url")
        if r["cyber_status"] == "no_provision_found" and not r["sources_searched"]:
            problems.append(f"{tag}: negative needs sources_searched")
        r["jurisdiction"] = JURIS.get(r["abbr"], "")
        r["epa2016_authorization"] = profiles.get(r["jurisdiction"], {}).get("authorization_2016", "") \
            if r["program"] == "drinking_water" else ""
        out.append(r)

    order = {a: i for i, a in enumerate(JURIS)}
    out.sort(key=lambda r: (order.get(r["abbr"], 99), r["program"]))
    cols = ["jurisdiction"] + REQUIRED_COLS + ["epa2016_authorization"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(out)

    by = {pg: Counter(r["cyber_status"] for r in out if r["program"] == pg) for pg in PROGRAMS}
    juris_any_required = sorted({r["abbr"] for r in out if r["cyber_status"] == "required"})
    req_dates = sorted((r["effective_date"], r["abbr"], r["program"]) for r in out
                       if r["cyber_status"] == "required")
    base = json.loads((ROOT / "data/processed/baseline_2016_stats.json").read_text())
    stats = {
        "n_jurisdictions": len(JURIS), "n_rows": len(out),
        "status_by_program": {pg: dict(by[pg]) for pg in PROGRAMS},
        "n_jurisdictions_any_required": len(juris_any_required),
        "jurisdictions_any_required": juris_any_required,
        "first_codified_required": req_dates[0] if req_dates else None,
        "required_timeline": req_dates,
        "n_verified_by_author": sum(r["verified_by_author"] == "yes" for r in out),
        "confidence": dict(Counter(r["confidence"].split(" ")[0] for r in out)),
        "jurisdictions_by_status": {s: sorted({r["abbr"] for r in out if r["cyber_status"] == s})
                                    for s in STATUS if s != "no_provision_found"},
        "n_jurisdictions_any_provision": len({r["abbr"] for r in out
                                              if r["cyber_status"] not in ("no_provision_found", "unknown")}),
        "positive_rows": [{k: r[k] for k in ("jurisdiction", "abbr", "program", "cyber_status", "mechanism",
                                              "hours", "cycle_years", "effective_date", "instrument_type", "citation")}
                          for r in out if r["cyber_status"] not in ("no_provision_found", "unknown")],
        "n_wpi_dw_treatment": sum(1 for r in out if r["program"] == "drinking_water"
                                  and r["exam_cyber_content"].startswith("yes")),
        "n_wpi_ww": sum(1 for r in out if r["program"] == "wastewater" and r["exam_provider"] == "WPI"),
        "n_rows_state_specific_source": sum(1 for r in out if r["confidence"] in ("medium", "high")),
        "n_rows_primary_text_high": sum(1 for r in out if r["confidence"] == "high"),
        "exam_cyber_by_program": {pg: dict(Counter(r["exam_cyber_content"].split(" ")[0]
                                                   for r in out if r["program"] == pg)) for pg in PROGRAMS},
        **base,
    }
    STATS.parent.mkdir(parents=True, exist_ok=True)
    STATS.write_text(json.dumps(stats, indent=2))

    with open(QA, "w", encoding="utf-8") as f:
        f.write("CERT-SCAN QA REPORT (DRAFT)\n\n")
        f.write(f"Rows: {len(out)} (expected {len(JURIS) * len(PROGRAMS)})\n")
        f.write(f"Problems: {len(problems)}\n")
        for p in problems:
            f.write(f"  - {p}\n")
        f.write("\nStatus by program:\n")
        for pg in PROGRAMS:
            f.write(f"  {pg}: {dict(by[pg])}\n")
        f.write(f"\nJurisdictions with any codified requirement: {juris_any_required}\n")
        f.write("Timeline of codified requirements:\n")
        for d in req_dates:
            f.write(f"  {d}\n")
        f.write("\nSpot checks for the author: every 'required' and 'credited_optional' row,\n"
                "plus OH and FL (negatives read from primary rule text).\n")
    print(json.dumps(stats, indent=2))
    print(f"{len(problems)} problems; see {QA}")
    return 1 if any(p.startswith(("DUPLICATE", "MISSING")) for p in problems) else 0


if __name__ == "__main__":
    sys.exit(main())
