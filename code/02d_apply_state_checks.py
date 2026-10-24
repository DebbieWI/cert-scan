#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: applies the results of the state-by-state checks
(data/processed/state_scan.csv plus pages read by hand through a web reader,
listed below) to the low-confidence rows in data/coding/coding.csv.
It only touches rows still at confidence 'low', so it never overwrites
anything the author has verified.
Do you need to open it? No.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODING = ROOT / "data/coding/coding.csv"
SCAN = ROOT / "data/processed/state_scan.csv"
SOURCES = ROOT / "data/coding/state_sources.csv"
TODAY = "2026-10-23"

# Pages scripts could not read, checked through the web reader on 2026-10-23.
MANUAL = {
    ("KS", "*"): ("https://www.kdhe.ks.gov/DocumentCenter/View/5187/Continuing-Education-Training-Credit-PDF",
                  "KDHE CE credit guide (updated 09/2026): training must be pertinent to operation; no cyber mention"),
    ("ME", "drinking_water"): ("https://www.maine.gov/dhhs/mecdc/sites/maine.gov.dhhs.mecdc/files/woRenewal.pdf",
                  "Renewal/upgrade form v.2026: TCH totals by class from approved course list; no cyber mention"),
    ("DE", "drinking_water"): ("https://dhss.delaware.gov/DPH/hsp/files/watroprnw.pdf",
                  "Renewal form (rev. 7/2023): 20 CEUs, at least 10 technical; no cyber mention"),
    ("DE", "wastewater"): ("https://dnrec.delaware.gov/water/commercial-government/wastewater-facilities/operators/",
                  "20 hours per 2 years, at least 10 in operations or maintenance; no cyber mention"),
    ("HI", "wastewater"): ("https://health.hawaii.gov/wastewater/files/2026/02/2026-Renewal-Application.pdf",
                  "2026 renewal application: 2 CEUs approved by Board; no topics named; no cyber mention"),
    ("IL", "wastewater"): ("https://ilga.gov/ftp/JCAR/AdminCode/035/035003800G07150R.html",
                  "35 Ill. Adm. Code 380.715: 20 hrs technical plus professional responsibility and safety; no cyber mention"),
    ("MA", "wastewater"): ("https://www.mass.gov/doc/257-cmr-2-certification-of-operators-of-wastewater-treatment-facilities/download",
                  "257 CMR 2.09(1): 10 TCH per year; no topics named; no cyber mention"),
    ("MS", "wastewater"): ("https://www.mdeq.ms.gov/water/field-services/wastewater-operator-trainer-certification-program/",
                  "MDEQ program page: no cyber mention (renewal form not reviewed)"),
    ("NH", "drinking_water"): ("https://des.nh.gov/water/drinking-water/public-water-systems/operator-certification",
                  "NHDES program page: no cyber mention (Env-Dw 502 text not reviewed)"),
    ("NH", "wastewater"): ("https://www.des.nh.gov/waste/wastewater/operator-certification",
                  "NHDES program page: CEUs per 2-year period, no topics named; no cyber mention"),
    ("CO", "*"): ("https://www.law.cornell.edu/regulations/colorado/5-CCR-1003-2-100.35",
                  "5 CCR 1003-2 Reg. 100.35 read; Board Guidance 19-1 mandatory regulatory training revised eff. 2025-01-01, "
                  "curriculum not reviewed [VERIFY whether it includes cybersecurity]"),
}
POSITIVE = {
    ("ME", "wastewater"): dict(
        cyber_status="credited_optional", mechanism="ce_eligible", instrument_type="guidance",
        citation="Maine DEP, TCH Requirements for Certification Renewal v1.3 (2022), Table 1",
        citation_url="https://www.maine.gov/dep/water/wwoperator/TCH%20Requirements%20for%20Certification%20Renewal%20V1.3%20-%20DEP%202022.pdf",
        effective_date="2022",
        evidence_note="DEP guidance lists cyber security as an acceptable operations and maintenance topic for renewal credit; no topic is required"),
    ("MT", "*"): dict(
        cyber_status="credited_optional", mechanism="ce_eligible", instrument_type="guidance",
        citation="Montana DEQ Continuing Education Credit Guidelines (2023-06-08), sections 3.1 and 5.2",
        citation_url="https://deq.mt.gov/files/Water/WQInfo/Documents/opcert/Forms/20230608_CEC_Guidelines_final.pdf",
        effective_date="2023-06-08",
        evidence_note="Cyber security courses qualify for full credit for water or wastewater operators; listed among approved safety topics"),
}
NOTES = {
    ("VT", "wastewater"): "Facility classification awards points for a computer-based control system (SCADA or DCS); no operator cyber training provision",
    ("WY", "*"): "DEQ operator certification page lists a CISA cybersecurity advisor contact; no operator cyber training provision",
    ("LA", "*"): "LAC 48:V ch. 73 not readable by script or web reader; LDH course approval form names no topics [VERIFY by hand]",
    ("DC", "*"): "No District operator certification program identified; DC Water material describes the certification requirement as applying everywhere outside Washington DC. DC lacks SDWA primacy (EPA Region 3) [VERIFY; author to decide how to present]",
}


def match(d, ab, pg):
    return d.get((ab, pg)) or d.get((ab, "*"))


def main():
    sources = {}
    for s in csv.DictReader(open(SOURCES, encoding="utf-8")):
        for pg in (("drinking_water", "wastewater") if s["program"] == "both" else (s["program"],)):
            sources.setdefault((s["abbr"], pg), s)
    scans = {}
    for r in csv.DictReader(open(SCAN, encoding="utf-8")):
        if r["readable"] != "yes":
            continue
        for pg in (("drinking_water", "wastewater") if r["program"] == "both" else (r["program"],)):
            scans.setdefault((r["abbr"], pg), r)
    # Minnesota and Mississippi: one shared rule / readable provider page
    if ("MN", "drinking_water") in scans:
        scans.setdefault(("MN", "wastewater"), scans[("MN", "drinking_water")])

    rows = list(csv.DictReader(open(CODING, newline="", encoding="utf-8")))
    cols = list(rows[0])
    changed = 0
    for r in rows:
        if r["confidence"] != "low":
            continue
        key = (r["abbr"], r["program"])
        src = sources.get(key)
        if src:
            r["certifying_body"] = src["certifying_body"]
            r["program_authority_citation"] = src["authority"]
        pos, man, scan = match(POSITIVE, *key), match(MANUAL, *key), scans.get(key)
        note = match(NOTES, *key)
        if pos:
            r.update(pos)
            r["sources_searched"] = f"Primary agency document read via web reader {TODAY}"
            r["confidence"] = "medium"
        elif scan:
            r.update(citation="renewal rule or program page", citation_url=scan["url"],
                     evidence_note=(note or f"Scanned {scan['words']} words; no cybersecurity provision found"),
                     sources_searched=f"Scripted scan of source text {TODAY} (data/processed/state_scan.csv)",
                     confidence="medium")
        elif man:
            r.update(citation="renewal rule or program page", citation_url=man[0], evidence_note=man[1],
                     sources_searched=f"Read via web reader {TODAY}", confidence="medium")
        elif note:
            r["evidence_note"] = note
            r["sources_searched"] = f"Attempted {TODAY}; primary text not readable"
        else:
            continue
        r["accessed"] = TODAY
        changed += 1
    with open(CODING, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    left = [(r["abbr"], r["program"]) for r in rows if r["confidence"] == "low"]
    print(f"updated {changed}; still low: {len(left)} {left}")


if __name__ == "__main__":
    main()
