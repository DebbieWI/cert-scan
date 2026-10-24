#!/usr/bin/env python3
"""
PLAIN-LANGUAGE HEADER
What this file does: adds rows to data/coding/coding.csv for every state and
program not yet hand-coded. Rows with a state-specific check get medium
confidence; rows covered only by the nationwide search sweep get LOW
confidence and are flagged for a state-specific check during verification.
It never overwrites a row already in the file.
Do you need to open it? No.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODING = ROOT / "data/coding/coding.csv"
TODAY = "2026-10-23"
SWEEP = ("Nationwide sweep, 9 queries (docs/SEARCH_LOG.md); no state-specific primary text read yet "
         "[VERIFY: read renewal rule]")

# State-specific checks done this session (agency page or rule text read; no cyber provision).
CHECKED = {
    ("CT", "drinking_water"): ("CT DPH Drinking Water Section", "Conn. Gen. Stat. 25-32n; RCSA 25-32-7a to -14",
        "https://portal.ct.gov/dph/drinking-water/dws/certificate-renewal-and-training",
        "Renewal and training page lists hour requirements; no cybersecurity mention"),
    ("CA", "drinking_water"): ("State Water Resources Control Board DDW", "Cal. H&S Code 106875-106910; 22 CCR 63750 et seq.",
        "https://www.waterboards.ca.gov/drinking_water/certlic/occupations/documents/opcert/renewalfaqs.pdf",
        "Renewal FAQ (updated Feb 2026) has no cybersecurity mention; regional cyber courses exist but no approval status found"),
    ("WA", "drinking_water"): ("WA Department of Health", "RCW 70.119; WAC 246-292",
        "https://www.doh.wa.gov/Portals/1/Documents/4200/OTS-3859-23Final.pdf",
        "2023 rule revision text (OTS-3859-23) has no cybersecurity mention"),
    ("WA", "wastewater"): ("WA Department of Ecology", "RCW 70A.212; WAC 173-230",
        "https://ecology.wa.gov/regulations-permits/permits-certifications/wastewater-operator-certification",
        "Ecology wastewater certification page has no cybersecurity mention"),
    ("AL", "drinking_water"): ("Alabama DEM", "Ala. Code 22-25-1 to -15; ADEM Admin. Code r. 335-10-1",
        "https://adem.alabama.gov/water/operator-certification/training",
        "ADEM training page has no cybersecurity mention"),
    ("AL", "wastewater"): ("Alabama DEM", "Ala. Code 22-25-1 to -15; ADEM Admin. Code r. 335-10-1",
        "https://adem.alabama.gov/water/operator-certification/training",
        "Same combined ADEM program and page"),
    ("IN", "wastewater"): ("Indiana DEM", "IC 13-18-11; 327 IAC 5-22 [VERIFY]",
        "https://www.in.gov/idem/cleanwater/wastewater-compliance/wastewater-operator-certification-and-continuing-education/wastewater-certification-information/",
        "Wastewater certification page mentions cybersecurity only as a site navigation link"),
    ("OH", None): None,
}

ALL = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA",
       "ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR",
       "PA","PR","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
NOTES = {
    ("TX", "wastewater"): "TCEQ resiliency CE requirement (RG-637) covers water operators only",
    ("MA", "wastewater"): "Separate Board of Certification of Operators of Wastewater Treatment Facilities not yet checked",
    ("NJ", "drinking_water"): "N.J. WQAA (2021 amendments) requires utility cybersecurity programs, not operator training; N.J.A.C. 7:10A not readable by script",
    ("NJ", "wastewater"): "Same combined N.J.A.C. 7:10A program",
    ("GA", "drinking_water"): "Ga. Comp. R. & Regs. 750 not readable by script; author's home state, check by hand",
    ("GA", "wastewater"): "Same combined Georgia board",
    ("DC", "drinking_water"): "Not in EPA 2016 report; confirm DC certifying body",
    ("DC", "wastewater"): "Not in EPA 2016 report; confirm DC certifying body",
    ("PR", "drinking_water"): "In EPA 2016 report (Act No. 53)",
}


def main():
    rows = list(csv.DictReader(open(CODING, newline="", encoding="utf-8")))
    cols = list(rows[0].keys())
    have = {(r["abbr"], r["program"]) for r in rows}
    added = 0
    for ab in ALL:
        for pg in ("drinking_water", "wastewater"):
            if (ab, pg) in have:
                continue
            r = {c: "" for c in cols}
            r.update(abbr=ab, program=pg, cyber_status="no_provision_found", mechanism="none",
                     instrument_type="none", exam_provider="[VERIFY]", exam_cyber_content="[VERIFY]",
                     accessed=TODAY, verified_by_author="no")
            chk = CHECKED.get((ab, pg))
            if chk:
                body, auth, url, note = chk
                r.update(certifying_body=body, program_authority_citation=auth, citation_url=url,
                         citation="program page or rule text", evidence_note=note,
                         sources_searched=f"State-specific page read; plus {SWEEP.split(' [')[0]}",
                         confidence="medium")
            else:
                r.update(certifying_body="[VERIFY]", program_authority_citation="[VERIFY]",
                         evidence_note=NOTES.get((ab, pg), ""), sources_searched=SWEEP, confidence="low")
            rows.append(r); added += 1
    with open(CODING, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f"added {added}; total {len(rows)}")


if __name__ == "__main__":
    main()
